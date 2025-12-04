from app.db.queries.rental_queries import RentalsQueries
from flask import current_app
import logging

from ..features.notifications.services import NotificationServices

from ..features.books.services import BookServices

from ..features.users.services import UserServices

from app.common.constants import NotificationMessages

logger = logging.getLogger(__name__)


class RentalStatusTask:
    @staticmethod
    def update_approved_to_pickup_confirmation():
        """
        Update rentals from 'approved' to 'awaiting_pickup_confirmation'
        when current time is within 1 hour before meetup.
        """
        db = current_app.extensions["db"]

        try:
            updated_rentals = db.fetch_all(
                RentalsQueries.UPDATE_APPROVED_TO_PICKUP_CONFIRMATION, ()
            )

            updated_count = len(updated_rentals) if updated_rentals else 0

            logger.info(
                f"✅ Updated {updated_count} rentals to awaiting_pickup_confirmation"
            )

            for updated_rental in updated_rentals:
                if updated_rental["book_id"]:
                    book_details = BookServices.get_book_details_service(
                        updated_rental["book_id"]
                    )

                    owner_id = (
                        str(book_details["owner_user_id"]) if book_details else None
                    )

                    owner_username = UserServices.get_username_service(owner_id)
                    renter_username = UserServices.get_username_service(
                        updated_rental["user_id"]
                    )

                    notification_header = NotificationMessages.PICKUP_REMINDER_HEADER

                    notification_message_renter = (
                        NotificationMessages.PICKUP_REMINDER_RENTER_MESSAGE.format(
                            title=f"{book_details['title'] if book_details else None}",
                            username=owner_username,
                            meetup_location=updated_rental["meetup_location"],
                        )
                    )

                    notification_message_owner = (
                        NotificationMessages.PICKUP_REMINDER_OWNER_MESSAGE.format(
                            title=f"{book_details['title'] if book_details else None}",
                            username=renter_username,
                            meetup_location=updated_rental["meetup_location"],
                        )
                    )

                    # Send notification to renter
                    NotificationServices.add_notification_service(
                        owner_id,
                        updated_rental["user_id"],
                        "rent",
                        notification_header,
                        notification_message_renter,
                    )

                    # Send notification to owner
                    NotificationServices.add_notification_service(
                        updated_rental["user_id"],
                        owner_id,
                        "rent",
                        notification_header,
                        notification_message_owner,
                    )

            return {
                "updated": updated_count,
                "rental_ids": (
                    [r["rental_id"] for r in updated_rentals] if updated_rentals else []
                ),
            }

        except Exception as e:
            logger.error(f"❌ Error updating rental statuses: {str(e)}")
            return {"updated": 0, "rental_ids": [], "error": str(e)}

    @staticmethod
    def update_ongoing_to_return_confirmation():
        """
        Update rentals from 'ongoing' to 'awaiting_return_confirmation'
        when current time is within 1 hour before return date.
        """
        db = current_app.extensions["db"]

        try:
            updated_rentals = db.fetch_all(
                RentalsQueries.UPDATE_ONGOING_TO_RETURN_CONFIRMATION, ()
            )

            updated_count = len(updated_rentals) if updated_rentals else 0

            logger.info(
                f"✅ Updated {updated_count} rentals to awaiting_return_confirmation"
            )

            for updated_rental in updated_rentals:
                if updated_rental["book_id"]:

                    book_details = BookServices.get_book_details_service(
                        updated_rental["book_id"]
                    )

                    owner_user_id = (
                        str(book_details["owner_user_id"]) if book_details else None
                    )

                    owner_username = UserServices.get_username_service(owner_user_id)
                    renter_username = UserServices.get_username_service(
                        updated_rental["user_id"]
                    )

                    notification_header = NotificationMessages.RETURN_REMINDER_HEADER

                    notification_message_renter = (
                        NotificationMessages.RETURN_REMINDER_RENTER_MESSAGE.format(
                            title=f"{book_details['title'] if book_details else None}",
                            meetup_location=updated_rental["meetup_location"],
                            username=owner_username,
                        )
                    )

                    notification_message_owner = (
                        NotificationMessages.RETURN_REMINDER_OWNER_MESSAGE.format(
                            title=f"{book_details['title'] if book_details else None}",
                            meetup_location=updated_rental["meetup_location"],
                            username=renter_username,
                        )
                    )

                    # Send notification to renter
                    NotificationServices.add_notification_service(
                        owner_user_id,
                        updated_rental["user_id"],
                        "rent",
                        notification_header,
                        notification_message_renter,
                    )

                    # Send notification to owner
                    NotificationServices.add_notification_service(
                        updated_rental["user_id"],
                        owner_user_id,
                        "rent",
                        notification_header,
                        notification_message_owner,
                    )

            return {
                "updated": updated_count,
                "rental_ids": (
                    [r["rental_id"] for r in updated_rentals] if updated_rentals else []
                ),
            }

        except Exception as e:
            logger.error(f"❌ Error updating rental statuses for returns: {str(e)}")
            return {"updated": 0, "rental_ids": [], "error": str(e)}
