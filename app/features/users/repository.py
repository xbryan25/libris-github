from app.db.queries.common import CommonQueries
from app.db.queries.user_queries import UserQueries
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
    def get_trust_score_stats() -> dict[str, float] | None:
        """
        Retrieve trust score statistics from all users.

        Returns:
            dict: A dictionary containing average trust score and total user count (None if no data).
        """

        db = current_app.extensions["db"]

        return db.fetch_one(
            UserQueries.GET_TRUST_SCORE_STATS,
            (),
        )

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
