from .repository import PurchasesRepository
from typing import Dict, Any
import traceback


class PurchasesService:

    @staticmethod
    def create_purchase_service(purchase_data: Dict[str, Any]) -> Dict[str, Any] | None:
        """
        Create a new purchase record in the database.

        Args:
            purchase_data (dict): Dictionary containing purchase details:
                - user_id
                - book_id
                - reserved_at
                - reservation_expires_at
                - total_buy_cost
                - meetup_time_window
                - meetup_location
                - meetup_date

        Returns:
            dict: The inserted purchase record if successful, None otherwise.
        """
        try:
            purchase = PurchasesRepository.insert_purchase(purchase_data)
            if not purchase:
                return None
            return purchase
        except Exception:
            traceback.print_exc()
            return None

    @staticmethod
    def check_pending_purchase(user_id: str, book_id: str) -> bool:
        """
        Check if the user already has a pending purchase for the given book.

        Returns:
            bool: True if a pending purchase exists, False otherwise.
        """
        try:
            return PurchasesRepository.exists_pending_purchase(user_id, book_id)
        except Exception:
            traceback.print_exc()
            return False
