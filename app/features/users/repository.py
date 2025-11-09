from app.db.queries.common import CommonQueries
from app.db.queries.user_queries import UserQueries
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
    def get_user_by_username(username: str) -> dict[str, str] | None:
        """
        Retrieve a user record from the database by username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            dict: A dictionary containing the user's details if found, otherwise None.
        """

        db = current_app.extensions["db"]

        return db.fetch_one(
            CommonQueries.GET_BY_SPECIFIC_COLUMN.format(
                table="users", column="username"
            ),
            (username,),
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
            CommonQueries.GET_COLUMN_BY_FIELD.format(
                column="username", table="users", field="user_id"
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

    @staticmethod
    def get_profile_info(user_id: str) -> dict[str, str] | None:
        """
        Retrieve the profile information of a user by their user_id.

        Args:
            user_id (str): The unique ID of the user.

        Returns:
            dict: A dictionary containing the user's profile information (None if no matching user).
        """

        db = current_app.extensions["db"]

        return db.fetch_one(
            UserQueries.GET_PROFILE_INFO,
            (user_id,),
        )

    @staticmethod
    def get_trust_score_percentile(user_id: str) -> dict[str, float] | None:
        """
        Retrieve the trust score percentile for a specific user.

        Args:
            user_id (str): The UUID of the user.

        Returns:
            dict: A dictionary containing trust_score_percentile (None if no data).
        """

        db = current_app.extensions["db"]

        stats = db.fetch_one(
            UserQueries.GET_TRUST_SCORE_PERCENTILE,
            (user_id,),
        )

        if not stats or "trust_score_percentile" not in stats:
            return None

        stats["trust_score_percentile"] = float(stats["trust_score_percentile"])

        return stats

    @staticmethod
    def update_user_profile(user_id: str, profile_data: dict) -> bool:
        """
        Update user profile information.

        Args:
            user_id (str): The unique ID of the user.
            profile_data (dict): Dictionary containing profile fields to update.

        Returns:
            bool: True if update was successful, False otherwise.
        """

        db = current_app.extensions["db"]

        try:
            db.execute_query(
                UserQueries.UPDATE_USER_PROFILE,
                (
                    profile_data.get("first_name"),
                    profile_data.get("middle_name"),
                    profile_data.get("last_name"),
                    profile_data.get("date_of_birth"),
                    profile_data.get("phone_number"),
                    profile_data.get("profile_image_url"),
                    user_id,
                ),
            )

            return True

        except Exception:
            return False

    @staticmethod
    def update_user_address(user_id: str, address_data: dict) -> bool:
        """
        Update user address information.

        Args:
            user_id (str): The unique ID of the user.
            address_data (dict): Dictionary containing address fields to update.

        Returns:
            bool: True if update was successful, False otherwise.
        """

        db = current_app.extensions["db"]

        try:
            current_user_address = UserRepository.get_user_address(user_id)

            if not current_user_address:
                db.execute_query(
                    UserQueries.INSERT_USER_ADDRESS,
                    (
                        address_data.get("country"),
                        address_data.get("city"),
                        address_data.get("barangay"),
                        address_data.get("street"),
                        address_data.get("postal_code"),
                        user_id,
                    ),
                )
            else:
                db.execute_query(
                    UserQueries.UPDATE_USER_ADDRESS,
                    (
                        address_data.get("country"),
                        address_data.get("city"),
                        address_data.get("barangay"),
                        address_data.get("street"),
                        address_data.get("postal_code"),
                        user_id,
                    ),
                )

            return True

        except Exception:
            return False

    @staticmethod
    def get_user_address(user_id: str) -> dict[str, str] | None:
        """
        Retrieve the address information of a user by their user_id.

        Args:
            user_id (str): The unique ID of the user.

        Returns:
            dict: A dictionary containing the user's address information (None if no matching user).
        """

        db = current_app.extensions["db"]

        return db.fetch_one(
            UserQueries.GET_USER_ADDRESS,
            (user_id,),
        )

    @staticmethod
    def get_user_profile(user_id: str) -> dict[str, str] | None:
        """
        Retrieve the profile information of a user by their user_id.

        Args:
            user_id (str): The unique ID of the user.

        Returns:
            dict: A dictionary containing the user's profile information (None if no matching user).
        """

        db = current_app.extensions["db"]

        return db.fetch_one(
            UserQueries.GET_USER_PROFILE,
            (user_id,),
        )

    @staticmethod
    def get_library_details(user_id: str) -> dict[str, int] | None:
        """
        Retrieve the number of owned, rented, and bought books for a specific user.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            dict: A dictionary containing the total number of books the user owns, has rented, and has bought, in the format:
                {
                    "owned_books": int,
                    "rented_books": int,
                    "bought_books": int
                }
        """

        db = current_app.extensions["db"]

        return db.fetch_one(
            UserQueries.GET_LIBRARY_DETAILS,
            (user_id, user_id, user_id),
        )
