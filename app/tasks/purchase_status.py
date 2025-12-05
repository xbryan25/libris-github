from app.db.queries.purchase_queries import PurchasesQueries
from flask import current_app
import logging

from ..features.notifications.services import NotificationServices

from ..features.books.services import BookServices

from ..features.users.services import UserServices

from app.common.constants import NotificationMessages

logger = logging.getLogger(__name__)


class PurchaseStatusTask:
    @staticmethod
    def update_approved_to_pickup_confirmation():
        """
        Update purchases from 'approved' to 'awaiting_pickup_confirmation'
        when current time is within 1 hour before meetup.
        """
        db = current_app.extensions["db"]

        try:
            updated_purchases = db.fetch_all(
                PurchasesQueries.UPDATE_APPROVED_TO_PICKUP_CONFIRMATION, ()
            )

            updated_count = len(updated_purchases) if updated_purchases else 0

            logger.info(
                f"✅ Updated {updated_count} purchases to awaiting_pickup_confirmation"
            )

            for updated_purchase in updated_purchases:
                if updated_purchase["book_id"]:

                    book_details = BookServices.get_book_details_service(
                        updated_purchase["book_id"]
                    )

                    owner_user_id = (
                        str(book_details["owner_user_id"]) if book_details else None
                    )

                    owner_username = UserServices.get_username_service(owner_user_id)
                    buyer_username = UserServices.get_username_service(
                        updated_purchase["user_id"]
                    )

                    notification_header = (
                        NotificationMessages.PURCHASE_PICKUP_REMINDER_HEADER
                    )

                    notification_message_renter = NotificationMessages.PURCHASE_PICKUP_REMINDER_BUYER_MESSAGE.format(
                        title=f"{book_details['title'] if book_details else None}",
                        meetup_location=updated_purchase["meetup_location"],
                        username=owner_username,
                    )

                    notification_message_owner = NotificationMessages.PURCHASE_PICKUP_REMINDER_OWNER_MESSAGE.format(
                        title=f"{book_details['title'] if book_details else None}",
                        meetup_location=updated_purchase["meetup_location"],
                        username=buyer_username,
                    )

                    # Send notification to buyer
                    NotificationServices.add_notification_service(
                        owner_user_id,
                        updated_purchase["user_id"],
                        "purchase",
                        notification_header,
                        notification_message_renter,
                    )

                    # Send notification to owner
                    NotificationServices.add_notification_service(
                        updated_purchase["user_id"],
                        owner_user_id,
                        "purchase",
                        notification_header,
                        notification_message_owner,
                    )

            return {
                "updated": updated_count,
                "purchase_ids": (
                    [r["purchase_id"] for r in updated_purchases]
                    if updated_purchases
                    else []
                ),
            }

        except Exception as e:
            logger.error(f"❌ Error updating purchase statuses: {str(e)}")
            return {"updated": 0, "purchase_ids": [], "error": str(e)}
