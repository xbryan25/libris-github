from app.db.queries.rental_queries import RentalsQueries
from flask import current_app
import logging

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
            result = db.fetch_all(
                RentalsQueries.UPDATE_APPROVED_TO_PICKUP_CONFIRMATION, ()
            )

            updated_count = len(result) if result else 0

            logger.info(
                f"✅ Updated {updated_count} rentals to awaiting_pickup_confirmation"
            )

            return {
                "updated": updated_count,
                "rental_ids": [r["rental_id"] for r in result] if result else [],
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
            result = db.fetch_all(
                RentalsQueries.UPDATE_ONGOING_TO_RETURN_CONFIRMATION, ()
            )

            updated_count = len(result) if result else 0

            logger.info(
                f"✅ Updated {updated_count} rentals to awaiting_return_confirmation"
            )

            return {
                "updated": updated_count,
                "rental_ids": [r["rental_id"] for r in result] if result else [],
            }

        except Exception as e:
            logger.error(f"❌ Error updating rental statuses for returns: {str(e)}")
            return {"updated": 0, "rental_ids": [], "error": str(e)}
