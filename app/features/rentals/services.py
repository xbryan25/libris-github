from .repository import RentalsRepository
from typing import Dict, Any
import traceback


class RentalsService:

    @staticmethod
    def create_rental_service(rental_data: Dict[str, Any]) -> Dict[str, Any] | None:
        """
        Create a new rental request in the database.

        Args:
            rental_data (dict): A dictionary containing rental details:
            - user_id
            - book_id
            - reserved_at
            - reservation_expires_at
            - total_rent_cost
            - rental_duration_days
            - meetup_time_window
            - meetup_location
            - meetup_date

        Returns:
            dict: The inserted rental record if successful, None otherwise.
        """
        try:
            rental = RentalsRepository.insert_rental(rental_data)
            if not rental:
                return None
            return rental
        except Exception:
            traceback.print_exc()
            return None

    @staticmethod
    def check_pending_rental(user_id: str, book_id: str) -> bool:
        """
        Check if the user already has a pending rental for the given book.

        Returns:
            bool: True if a pending rental exists, False otherwise.
        """
        try:
            return RentalsRepository.exists_pending_rental(user_id, book_id)
        except Exception:
            traceback.print_exc()
            return False
