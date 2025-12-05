from app.db.queries.purchase_queries import PurchasesQueries
from flask import current_app
import logging

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
            result = db.fetch_all(
                PurchasesQueries.UPDATE_APPROVED_TO_PICKUP_CONFIRMATION, ()
            )

            updated_count = len(result) if result else 0

            logger.info(
                f"✅ Updated {updated_count} purchases to awaiting_pickup_confirmation"
            )

            return {
                "updated": updated_count,
                "purchase_ids": [r["purchase_id"] for r in result] if result else [],
            }

        except Exception as e:
            logger.error(f"❌ Error updating purchase statuses: {str(e)}")
            return {"updated": 0, "purchase_ids": [], "error": str(e)}
