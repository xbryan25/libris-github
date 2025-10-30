from .repository import UserRepository

from app.common.dataclasses import User

from app.utils import convert_user_dict

from typing import Any


class UserServices:

    @staticmethod
    def user_login_service(email_address: str, password: str) -> User | None:
        """
        Authenticate a user with email address and password.

        Args:
            email_address (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: A User dataclass instance if credentials are correct, otherwise None.
        """

        user = UserRepository.get_user_by_email_address(email_address)

        if not user:
            return None

        user["user_id"] = str(user["user_id"])

        # Convert dict to dataclass
        user_dataclass = convert_user_dict(user)

        # Verify password
        if user_dataclass.check_password(password):
            return user_dataclass

        return None

    @staticmethod
    def get_username_service(user_id) -> str | None:
        """
        Get the username of a user using the user_id.

        Args:
            user_id (str): user_id of the user.

        Returns:
            str: The username of the user if found, otherwise None.
        """

        username_dict = UserRepository.get_username(user_id)

        if username_dict is None:
            return None

        return username_dict["username"]

    @staticmethod
    def get_profile_info_service(user_id: str) -> dict[str, Any] | None:
        """
        Get the profile information of a user using the user_id.

        Args:
            user_id (str): user_id of the user.

        Returns:
            dict: A dictionary containing the user's profile information (None if no matching user).
        """

        profile_info = UserRepository.get_profile_info(user_id)

        return profile_info

    @staticmethod
    def get_user_address_service(user_id: str) -> dict[str, str] | None:
        """
        Get the address information of a user using the user_id.

        Args:
            user_id (str): user_id of the user.

        Returns:
            dict: A dictionary containing the user's address information (None if no matching user).
        """

        address_info = UserRepository.get_user_address(user_id)

        return address_info

    @staticmethod
    def update_user_profile_service(user_id: str, profile_data: dict) -> bool:
        """
        Update user profile information while preserving existing values
        when only some fields are sent (e.g., only updating profile image).
        """
        try:
            existing_profile = UserRepository.get_user_profile(user_id)
            if not existing_profile:
                return False

            # Merge existing data with incoming data — only overwrite provided keys
            merged_data = existing_profile.copy()
            merged_data.update({k: v for k, v in profile_data.items() if v is not None})

            return UserRepository.update_user_profile(user_id, merged_data)

        except Exception as e:
            print("Error updating user profile:", e)
            return False

    @staticmethod
    def update_user_address_service(user_id: str, address_data: dict) -> bool:
        """
        Update user address information.

        Args:
            user_id (str): The unique ID of the user.
            address_data (dict): Dictionary containing address fields to update.

        Returns:
            bool: True if update was successful, False otherwise.
        """

        return UserRepository.update_user_address(user_id, address_data)

    @staticmethod
    def get_trust_score_comparison_service(user_id: str) -> dict[str, Any] | None:
        """
        Get trust score percentile for a user.

        Args:
            user_id (str): The UUID of the user.

        Returns:
            dict: A dictionary containing trust_score_percentile (None if no data).
        """
        stats = UserRepository.get_trust_score_percentile(user_id)

        if not stats or stats.get("trust_score_percentile") is None:
            return None

        percentile = float(stats["trust_score_percentile"])

        return {
            "user_id": user_id,
            "trust_score_percentile": round(percentile, 1),
            "is_above_average": percentile > 50,
        }

    @staticmethod
    def get_library_details_service(user_id) -> dict[str, int] | None:
        """
        Retrieve the number of owned, rented, and bought books for a specific user.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            dict: A dictionary containing the counts of books associated with the user, with the following keys:
                - owned (int): The number of books the user owns.
                - rented (int): The total number of books the user has rented (past and present).
                - bought (int): The number of books the user has purchased.
        """

        library_details_dict = UserRepository.get_library_details(user_id)

        if library_details_dict is None:
            return None

        return library_details_dict
