from flask import current_app
from app.db.queries.rental_queries import RentalsQueries
import uuid


class RentalsRepository:

    @staticmethod
    def insert_rental(rental_data: dict) -> dict | None:
        """
        Insert a new rental record into the database with proper defaults.

        Args:
            rental_data (dict): Dictionary containing rental details:
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
            str: The rental_id of the inserted rental, or None if insertion failed.
        """
        db = current_app.extensions["db"]

        rental_id = str(uuid.uuid4())

        params = (
            rental_id,
            rental_data["user_id"],
            rental_data["book_id"],
            "pending",
            rental_data["reserved_at"],
            rental_data["reservation_expires_at"],
            rental_data["total_rent_cost"],
            rental_data["rental_duration_days"],
            False,
            rental_data["meetup_time_window"],
            rental_data["meetup_location"],
            rental_data["meetup_date"],
        )

        result = db.fetch_one(RentalsQueries.INSERT_RENTAL, params)

        if result:
            rental_data["rental_id"] = result["rental_id"]
            return rental_data

        return None
