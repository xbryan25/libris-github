from .repository import UserRepository

from app.common.dataclasses import User

from app.utils import convert_user_dict


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

        user_dataclass = convert_user_dict(user)

        if user_dataclass.check_password(password):
            return user_dataclass

        return None

    @staticmethod
    def user_signup_service(
        username: str, email_address: str, password: str
    ) -> dict | None:
        """
        Create a new user account and initialize their wallet.

        Args:
            username (str): The desired username.
            email_address (str): The email address of the user.
            password (str): The password for the account.

        Returns:
            dict: Success message if user created, None if email already exists.
        """

        existing_user = UserRepository.get_user_by_email_address(email_address)

        if existing_user:
            return None

        user_id = UserRepository.create_user(username, email_address, password)

        UserRepository.initialize_wallet(user_id)

        return {"success": True}

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
