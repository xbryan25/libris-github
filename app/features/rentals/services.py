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
                - rental_id: UUID of the rental
                - user_id: UUID of the user
                - book_id: UUID of the book
                - rent_status: "pending"
                - reserved_at: timestamp of request
                - reservation_expires_at: timestamp + 1 day
                - total_rent_cost: total cost of rental
                - rental_duration_days: number of days
                - all_fees_captured: False
                - meetup_time_window: preferred time window
                - meetup_location: meetup location
                - meetup_date: date of meetup

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
