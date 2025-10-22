from app.db.queries.common import CommonQueries

from flask import current_app


class UserRepository:

    @staticmethod
    def get_user_by_email_address(email_address: str) -> dict[str, str] | None:
        """
        Retrieve a user record from the database by email address.

        Args:
            email_address (str): The email address of the user to retrieve.

        Returns:
            dict: A dictionary containing the user's details if found, otherwise None.
        """

        db = current_app.extensions["db"]

        return db.fetch_one(
            CommonQueries.GET_BY_SPECIFIC_COLUMN.format(
                table="users", column="email_address"
            ),
            (email_address,),
        )

    @staticmethod
    def get_username(user_id: str) -> dict[str, str] | None:
        """
        Retrieve the username of a user by their user_id.

        Args:
            user_id (str): The unique ID of the user.

        Returns:
            dict: A dictionary containing the user's username in the format (None if no matching user):
                {"username": str}
        """

        db = current_app.extensions["db"]

        return db.fetch_one(
            CommonQueries.GET_COLUMN_BY_PK.format(
                column="username", table="users", pk="user_id"
            ),
            (user_id,),
        )
