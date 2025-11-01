from app.db.queries.common import CommonQueries

from flask import current_app

from werkzeug.security import generate_password_hash


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

    @staticmethod
    def create_user(username: str, email_address: str, password: str) -> str:
        """
        Create a new user in the database.

        Args:
            username (str): The username for the new user.
            email_address (str): The email address for the new user.
            password (str): The plain text password (will be hashed).

        Returns:
            str: The user_id of the newly created user.
        """

        db = current_app.extensions["db"]

        hashed_password = generate_password_hash(password)

        result = db.fetch_one(
            "INSERT INTO users (username, email_address, password_hash, trust_score) VALUES (%s, %s, %s, 0) RETURNING user_id",
            (username, email_address, hashed_password),
        )

        return str(result["user_id"])

    @staticmethod
    def initialize_wallet(user_id: str) -> None:
        """
        Initialize a wallet for a new user with balance of 0.

        Args:
            user_id (str): The user_id of the user to initialize wallet for.
        """

        db = current_app.extensions["db"]

        db.execute_query(
            "INSERT INTO readits_wallets (user_id, balance) VALUES (%s, %s)",
            (user_id, 0),
        )
