from flask import current_app
from datetime import datetime, timezone
import logging

from ..features.notifications.services import NotificationServices

from ..features.books.services import BookServices

from ..features.users.services import UserServices

from app.common.constants import NotificationMessages

logger = logging.getLogger(__name__)


class RentalCleanupTask:
    @staticmethod
    def cleanup_expired_rentals():
        """
        Clean up expired rental requests.
        This task:
        1. Finds all pending rentals where reservation_expires_at < now
        2. Releases reserved funds for each expired rental
        3. Deletes the expired rental entries
        """
        try:
            db = current_app.extensions["db"]

            # Get current time in UTC
            now = datetime.now(timezone.utc)

            print(f"Current time (UTC): {now}")

            # Get all expired pending rentals
            query = """
                SELECT
                    rb.rental_id,
                    rb.user_id,
                    rb.book_id,
                    rb.total_rent_cost,
                    rb.reservation_expires_at
                FROM rented_books rb
                WHERE rb.rent_status = 'pending'
                AND rb.reservation_expires_at < (NOW() AT TIME ZONE 'UTC' + INTERVAL '8 hours');
            """

            expired_rentals = db.fetch_all(query, ())

            print(
                f"Found {len(expired_rentals) if expired_rentals else 0} expired rentals"
            )

            if expired_rentals:
                for r in expired_rentals:
                    print(
                        f"  - Rental {r.get('rental_id')}: expires at {r.get('reservation_expires_at')}"
                    )

            if not expired_rentals:
                logger.info("No expired rentals found.")
                return {"cleaned": 0, "errors": 0}

            cleaned_count = 0
            error_count = 0

            for rental in expired_rentals:
                rental_id = rental.get("rental_id")
                user_id = str(rental.get("user_id"))
                total_cost = int(rental.get("total_rent_cost", 0))

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
                        release_query, (total_cost, now, user_id, total_cost)
                    )

                    if not wallet_result:
                        logger.warning(
                            f"Failed to release funds for expired rental {rental_id}. "
                            f"User: {user_id}, Amount: {total_cost}"
                        )

                    # Delete the rental entry
                    delete_query = """
                        DELETE FROM rented_books
                        WHERE rental_id = %s
                        AND rent_status = 'pending'
                        RETURNING rental_id;
                    """

                    delete_result = db.fetch_one(delete_query, (rental_id,))

                    book_details = BookServices.get_book_details_service(
                        rental.get("book_id")
                    )

                    owner_id = (
                        str(book_details["owner_user_id"]) if book_details else None
                    )

                    owner_username = UserServices.get_username_service(owner_id)

                    notification_header = (
                        NotificationMessages.RENTAL_REQUEST_EXPIRED_HEADER
                    )
                    notification_message = (
                        NotificationMessages.RENTAL_REQUEST_EXPIRED_MESSAGE.format(
                            title=f"{book_details['title'] if book_details else None}",
                            username=owner_username,
                        )
                    )

                    NotificationServices.add_notification_service(
                        owner_id,
                        user_id,
                        "rent",
                        notification_header,
                        notification_message,
                    )

                    if delete_result:
                        cleaned_count += 1
                        logger.info(
                            f"Cleaned up expired rental {rental_id}. "
                            f"Released {total_cost} readits for user {user_id}."
                        )
                    else:
                        error_count += 1
                        logger.error(f"Failed to delete expired rental {rental_id}")

                except Exception as e:
                    error_count += 1
                    logger.error(f"Error cleaning up rental {rental_id}: {str(e)}")

            logger.info(
                f"Cleanup completed. Cleaned: {cleaned_count}, Errors: {error_count}"
            )

            return {"cleaned": cleaned_count, "errors": error_count}

        except Exception as e:
            logger.error(f"Error in cleanup_expired_rentals: {str(e)}")
            return {"cleaned": 0, "errors": 1}
