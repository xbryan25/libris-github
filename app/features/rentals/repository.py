from app.db.queries.rentals import RentalQueries
from flask import current_app
from typing import Any


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
