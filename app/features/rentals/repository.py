from app.db.queries.rentals import RentalQueries
from flask import current_app
from typing import Any
import logging

logger = logging.getLogger(__name__)


class RentalRepository:
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

        result = db.fetch_all(RentalQueries.GET_USER_RENTALS_WITH_STATUS, params)
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

        result = db.fetch_all(RentalQueries.GET_USER_LENDINGS_WITH_STATUS, params)
        return result if result else []

    @staticmethod
    def get_rental_by_id(rental_id: str) -> dict[str, Any] | None:
        """
        Retrieve rental details by rental ID.
        """
        db = current_app.extensions["db"]
        params = (rental_id,)
        result = db.fetch_one(RentalQueries.GET_RENTAL_BY_ID, params)
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

        result = db.fetch_one(RentalQueries.APPROVE_RENTAL, params)

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

        result = db.fetch_one(RentalQueries.DELETE_RENTAL, params)

        return result
