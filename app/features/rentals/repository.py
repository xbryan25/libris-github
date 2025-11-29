from app.db.queries.rental_queries import RentalsQueries
from flask import current_app
from typing import Any
import logging

logger = logging.getLogger(__name__)


class RentalsRepository:
    @staticmethod
    def get_user_rentals_with_status(user_id: str) -> list[dict[str, Any]]:
        """
        Retrieve all rentals for a user with statuses.

        Args:
            user_id (str): The ID of the user whose rentals are being fetched.

        Returns:
            list[dict[str, Any]]: A list of rental dictionaries with book and owner details.
                Returns empty list if no rentals found.
        """
        db = current_app.extensions["db"]
        params = (user_id,)

        result = db.fetch_all(RentalsQueries.GET_USER_RENTALS_WITH_STATUS, params)
        return result if result else []

    @staticmethod
    def get_user_lendings_with_status(user_id: str) -> list[dict[str, Any]]:
        """
        Retrieve all lendings for a user with statuses.

        Args:
            user_id (str): The ID of the user whose lendings are being fetched.

        Returns:
            list[dict[str, Any]]: A list of lending dictionaries with book and borrower details.
                Returns empty list if no lendings found.
        """
        db = current_app.extensions["db"]
        params = (user_id,)

        result = db.fetch_all(RentalsQueries.GET_USER_LENDINGS_WITH_STATUS, params)
        return result if result else []

    @staticmethod
    def get_rental_by_id(rental_id: str) -> dict[str, Any] | None:
        """
        Retrieve rental details by rental ID.
        """
        db = current_app.extensions["db"]
        params = (rental_id,)
        result = db.fetch_one(RentalsQueries.GET_RENTAL_BY_ID, params)
        return result

    @staticmethod
    def approve_rental(rental_id: str, meetup_time: str) -> dict[str, Any] | None:
        """
        Approve a rental and set meetup time.

        Args:
            rental_id (str): The rental ID to approve.
            meetup_time (str): The meetup time (HH:MM format).

        Returns:
            dict[str, Any] | None: Updated rental details or None if update failed.
        """
        db = current_app.extensions["db"]
        params = (meetup_time, rental_id)

        result = db.fetch_one(RentalsQueries.APPROVE_RENTAL, params)

        return result

    @staticmethod
    def delete_rental(rental_id: str) -> dict[str, Any] | None:
        """
        Delete a rental entry from rented_books.

        Args:
            rental_id (str): The rental ID to delete.

        Returns:
            dict[str, Any] | None: Deleted rental ID or None if deletion failed.
        """
        db = current_app.extensions["db"]
        params = (rental_id,)

        result = db.fetch_one(RentalsQueries.DELETE_RENTAL, params)

        return result

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
                - actual_rate
                - actual_deposit

        Returns:
            str: The rental_id of the inserted rental, or None if insertion failed.
        """
        db = current_app.extensions["db"]

        params = (
            rental_data["user_id"],
            rental_data["book_id"],
            rental_data["reserved_at"],
            rental_data["reservation_expires_at"],
            rental_data["total_rent_cost"],
            rental_data["rental_duration_days"],
            rental_data["meetup_time_window"],
            rental_data["meetup_location"],
            rental_data["meetup_date"],
            rental_data["actual_rate"],
            rental_data["actual_deposit"],
        )

        result = db.fetch_one(RentalsQueries.INSERT_RENTAL, params)

        if result:
            rental_data["rental_id"] = result["rental_id"]
            return rental_data

        return None

    @staticmethod
    def exists_pending_rental(user_id: str, book_id: str) -> bool:
        """
        Check if a pending rental exists for the given user and book.

        Returns:
            bool: True if a pending rental exists, False otherwise.
        """
        db = current_app.extensions["db"]

        result = db.fetch_one(RentalsQueries.CHECK_PENDING_RENTAL, (user_id, book_id))
        return bool(result)

    @staticmethod
    def get_rental_by_id_full(rental_id: str) -> dict[str, Any] | None:
        """
        Retrieve full rental details by rental ID including confirmation statuses.
        """
        db = current_app.extensions["db"]
        params = (rental_id,)
        result = db.fetch_one(RentalsQueries.GET_RENTAL_BY_ID_FULL, params)
        return result

    @staticmethod
    def confirm_pickup(
        rental_id: str, is_owner: bool, is_renter: bool, rental_duration: int
    ) -> dict[str, Any] | None:
        """
        Confirm pickup by owner or renter.
        If both have confirmed, update status to 'ongoing' and set rent_start/end_date.
        """
        db = current_app.extensions["db"]

        params = (
            is_owner,
            is_renter,
            is_owner,
            is_renter,
            is_owner,
            is_renter,
            is_owner,
            is_renter,
            rental_duration,
            rental_id,
        )

        result = db.fetch_one(RentalsQueries.CONFIRM_PICKUP, params)
        return result

    @staticmethod
    def get_rental_by_id_full_return(rental_id: str) -> dict[str, Any] | None:
        """
        Retrieve full rental details by rental ID including return confirmation statuses.
        """
        db = current_app.extensions["db"]
        params = (rental_id,)
        result = db.fetch_one(RentalsQueries.GET_RENTAL_BY_ID_FULL_RETURN, params)
        return result

    @staticmethod
    def confirm_return(
        rental_id: str, is_owner: bool, is_renter: bool
    ) -> dict[str, Any] | None:
        """
        Confirm return by owner or renter.
        If both have confirmed, update status to 'completed'.
        """
        db = current_app.extensions["db"]

        params = (
            is_owner,
            is_renter,
            is_owner,
            is_renter,
            rental_id,
        )

        result = db.fetch_one(RentalsQueries.CONFIRM_RETURN, params)
        return result

    @staticmethod
    def check_book_availability(book_id: str, owner_id: str) -> dict[str, Any] | None:
        """
        Check if a book already has an active rental (approved or ongoing).

        Args:
            book_id (str): The book ID to check
            owner_id (str): The owner ID to verify ownership

        Returns:
            dict with rental details if book is unavailable, None if available
        """
        db = current_app.extensions["db"]
        params = (book_id, owner_id)
        result = db.fetch_one(RentalsQueries.CHECK_BOOK_AVAILABILITY, params)
        return result

    @staticmethod
    def get_book_id_from_rental(rental_id: str) -> str | None:
        """
        Get the book_id for a given rental.

        Args:
            rental_id (str): The rental ID

        Returns:
            str: The book_id or None if not found
        """
        db = current_app.extensions["db"]
        result = db.fetch_one(RentalsQueries.GET_BOOK_ID_FROM_RENTAL, (rental_id,))
        return result.get("book_id") if result else None
