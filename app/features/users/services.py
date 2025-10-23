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
