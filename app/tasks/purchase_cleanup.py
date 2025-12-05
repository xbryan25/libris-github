from flask import current_app
from datetime import datetime, timezone
import logging

from ..features.notifications.services import NotificationServices

from ..features.books.services import BookServices

from ..features.users.services import UserServices

from app.common.constants import NotificationMessages

logger = logging.getLogger(__name__)


class PurchaseCleanupTask:
    @staticmethod
    def cleanup_expired_purchases():
        """
        Clean up expired purchase requests.
        This task:
        1. Finds all pending purchases where reservation_expires_at < now
        2. Releases reserved funds for each expired purchase
        3. Deletes the expired purchase entries
        """
        try:
            db = current_app.extensions["db"]

            # Get current time in UTC
            now = datetime.now(timezone.utc)

            # Get all expired pending purchases
            query = """
                SELECT
                    pb.purchase_id,
                    pb.user_id,
                    pb.total_buy_cost,
                    pb.reservation_expires_at
                FROM purchased_books pb
                WHERE pb.purchase_status = 'pending'
                AND pb.reservation_expires_at < (NOW() AT TIME ZONE 'UTC' + INTERVAL '8 hours');
            """

            expired_purchases = db.fetch_all(query, ())

            if not expired_purchases:
                logger.info("No expired purchases found.")
                return {"cleaned": 0, "errors": 0}

            cleaned_count = 0
            error_count = 0

            for purchase in expired_purchases:
                purchase_id = purchase.get("purchase_id")
                buyer_id = str(purchase.get("user_id"))
                total_cost = int(purchase.get("total_buy_cost", 0))

                try:
                    # Release reserved funds
                    release_query = """
                        UPDATE readits_wallets
                        SET
                            reserved_amount = reserved_amount - %s,
                            last_updated = %s
                        WHERE user_id = %s
                        AND reserved_amount >= %s
                        RETURNING wallet_id;
                    """

                    wallet_result = db.fetch_one(
                        release_query, (total_cost, now, buyer_id, total_cost)
                    )

                    if not wallet_result:
                        logger.warning(
                            f"Failed to release funds for expired purchase {purchase_id}. "
                            f"User: {buyer_id}, Amount: {total_cost}"
                        )

                    # Delete the purchase entry
                    delete_query = """
                        DELETE FROM purchased_books
                        WHERE purchase_id = %s
                        AND purchase_status = 'pending'
                        RETURNING purchase_id;
                    """

                    delete_result = db.fetch_one(delete_query, (purchase_id,))

                    book_details = BookServices.get_book_details_service(
                        purchase.get("book_id")
                    )

                    owner_id = (
                        str(book_details["owner_user_id"]) if book_details else None
                    )

                    owner_username = UserServices.get_username_service(owner_id)

                    notification_header = (
                        NotificationMessages.PURCHASE_REQUEST_EXPIRED_HEADER
                    )
                    notification_message = (
                        NotificationMessages.PURCHASE_REQUEST_EXPIRED_MESSAGE.format(
                            title=f"{book_details['title'] if book_details else None}",
                            username=owner_username,
                        )
                    )

                    NotificationServices.add_notification_service(
                        owner_id,
                        buyer_id,
                        "rent",
                        notification_header,
                        notification_message,
                    )

                    if delete_result:
                        cleaned_count += 1
                        logger.info(
                            f"Cleaned up expired purchase {purchase_id}. "
                            f"Released {total_cost} readits for user {buyer_id}."
                        )
                    else:
                        error_count += 1
                        logger.error(f"Failed to delete expired purchase {purchase_id}")

                except Exception as e:
                    error_count += 1
                    logger.error(f"Error cleaning up purchase {purchase_id}: {str(e)}")

            logger.info(
                f"Cleanup completed. Cleaned: {cleaned_count}, Errors: {error_count}"
            )

            return {"cleaned": cleaned_count, "errors": error_count}

        except Exception as e:
            logger.error(f"Error in cleanup_expired_purchases: {str(e)}")
            return {"cleaned": 0, "errors": 1}
