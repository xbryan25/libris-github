from .repository import UserRepository
from typing import Any
from app.common.dataclasses import User
from app.utils import convert_user_dict
import random
from datetime import datetime, timedelta, timezone
from app.services.email_service import EmailService
from app.utils.password_validator import PasswordValidator
from app.exceptions.custom_exceptions import (
    EmailInUseByGoogleError,
    EntityNotFoundError,
)


class UserServices:

    @staticmethod
    def user_login_service(email_address: str, password: str) -> User | None:
        """Authenticate user with email address and password."""
        user = UserRepository.get_user_by_email_address(email_address)

        if not user:
            return None

        if user and user["auth_provider"] == "google":
            raise EmailInUseByGoogleError(
                "Email address is linked to a Google account. Try logging in using Google."
            )

        user["user_id"] = str(user["user_id"])
        user_dataclass = convert_user_dict(user)

        if user_dataclass.check_password(password):
            return user_dataclass

        return None

    @staticmethod
    def user_signup_service(
        username: str, email_address: str, password: str
    ) -> dict | None:
        """Create new user account and initialize wallet."""

        # Validate password strength BEFORE creating user
        validation = PasswordValidator.validate_password(
            password, username or "", email_address or ""
        )

        if not validation["valid"]:
            print(
                f"[SIGNUP SERVICE] Password validation failed: {validation['errors']}"
            )
            return {"error": validation["errors"][0], "type": "password"}

        existing_user_by_email = UserRepository.get_user_by_email_address(email_address)

        if existing_user_by_email:
            if existing_user_by_email["auth_provider"] == "google":
                return {
                    "error": "Email address is already linked to a Google account.",
                    "type": "email",
                }
            else:
                return {"error": "Email address is already in use.", "type": "email"}

        existing_user_by_username = UserRepository.get_user_by_username(username)

        if existing_user_by_username:

            return {"error": "Username already exists.", "type": "username"}

        user_id = UserRepository.create_user(username, email_address, password)

        UserRepository.initialize_wallet(user_id)

        return {"success": True, "user_id": user_id}

    @staticmethod
    def generate_verification_code() -> str:
        """Generate random 6-digit verification code."""
        code = str(random.randint(100000, 999999))

        return code

    @staticmethod
    def send_verification_email_service(user_id: str) -> dict:
        """Generate verification code, store it, and send email."""
        try:
            user_data = UserRepository.get_user_email_and_username(user_id)

            if not user_data:
                return {"error": "User not found."}

            # Generate new code
            code = UserServices.generate_verification_code()

            # Set expiration time (10 minutes from now)
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

            # Store code in database (old codes are deleted automatically)
            success = UserRepository.create_verification_code(user_id, code, expires_at)

            if not success:
                return {"error": "Failed to create verification code."}

            email_sent = EmailService.send_verification_email(
                user_data["email_address"], code, user_data["username"]
            )

            if not email_sent:

                return {"error": "Failed to send verification email."}

            return {
                "success": True,
                "message": "Verification email sent successfully.",
            }

        except Exception:
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    @staticmethod
    def verify_email_code_service(
        user_id: str, code: str, account_activated_at: datetime
    ) -> dict:
        """Verify the email verification code."""
        try:

            if UserRepository.is_email_verified(user_id):
                return {"error": "Email is already verified."}

            is_valid = UserRepository.verify_email_code(user_id, code)

            if not is_valid:

                return {"error": "Invalid or expired verification code."}

            success = UserRepository.mark_email_as_verified(user_id)

            if not success:

                return {"error": "Failed to verify email."}

            else:
                UserRepository.update_account_activated_at(
                    user_id, account_activated_at
                )

                return {
                    "success": True,
                    "message": "Email verified successfully!",
                }

        except Exception:

            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    @staticmethod
    def user_google_signup_service(
        email_address: str,
        first_name: str,
        last_name: str,
        profile_image_url: str | None,
        account_activated_at: datetime,
    ) -> str | None:
        """
        add later
        """
        user_id = UserRepository.create_user_from_google(
            email_address, first_name, last_name, profile_image_url
        )

        UserRepository.initialize_wallet(user_id)

        UserRepository.update_account_activated_at(user_id, account_activated_at)

        return user_id

    @staticmethod
    def update_username_by_user_id_service(user_id: str, username: str) -> None:
        """
        add later
        """
        UserRepository.update_username_by_user_id(user_id, username)

    @staticmethod
    def get_user_info_service(user_id) -> dict[str, str | bool]:
        """Get the username, email verification status, and auth provider of a user using the user_id."""
        user_dict = UserRepository.get_user_info(user_id)

        if user_dict is None:
            raise EntityNotFoundError("User not authorized.")

        return user_dict

    @staticmethod
    def get_username_service(user_id) -> str | None:
        """Get the username of a user using the user_id."""
        username_dict = UserRepository.get_username(user_id)

        if username_dict is None:
            return None

        return username_dict["username"]

    @staticmethod
    def check_if_username_is_taken_service(username: str) -> bool:
        """
        Get the username of a user using the user_id.

        Args:
            user_id (str): user_id of the user.

        Returns:
            str: The username of the user if found, otherwise None.
        """
        is_username_taken = UserRepository.check_if_username_is_taken(username)

        return is_username_taken["exists"]

    @staticmethod
    def get_user_by_email_address_service(email: str) -> dict[str, Any] | None:
        """
        Retrieve a user and their details using an email.

        Args:
            email (str): The email used to retreive a user.

        Returns:
            str: The username of the user if found, otherwise None.
        """
        user_dict = UserRepository.get_user_by_email_address(email)

        if user_dict is None:
            return None

        return user_dict

    @staticmethod
    def get_profile_info_service(user_id: str) -> dict[str, Any] | None:
        """Get the profile information of a user using the user_id."""
        profile_info = UserRepository.get_profile_info(user_id)

        return profile_info

    @staticmethod
    def get_user_address_service(user_id: str) -> dict[str, str] | None:
        """Get the address information of a user using the user_id."""
        address_info = UserRepository.get_user_address(user_id)

        return address_info

    @staticmethod
    def update_user_profile_service(user_id: str, profile_data: dict) -> bool:
        """Update user profile while preserving existing values."""
        try:
            existing_profile = UserRepository.get_user_profile(user_id)

            if not existing_profile:
                return False

            merged_data = existing_profile.copy()
            merged_data.update({k: v for k, v in profile_data.items() if v is not None})

            return UserRepository.update_user_profile(user_id, merged_data)

        except Exception:
            return False

    @staticmethod
    def update_user_address_service(user_id: str, address_data: dict) -> bool:
        """Update user address information."""
        return UserRepository.update_user_address(user_id, address_data)

    @staticmethod
    def get_trust_score_comparison_service(
        user_id: str,
    ) -> dict[str, Any] | None:
        """Get trust score percentile for a user."""
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
        """Retrieve book counts for a specific user."""
        library_details_dict = UserRepository.get_library_details(user_id)

        if library_details_dict is None:
            return None

        return library_details_dict

    # PASSWORD RESET METHODS

    @staticmethod
    def request_password_reset_service(email_address: str) -> dict:
        """Send password reset code to user's email."""
        try:
            print(
                f"[PASSWORD RESET SERVICE] Starting password reset for email: {email_address}"
            )

            # Get user by email
            user = UserRepository.get_user_by_email_for_reset(email_address)

            if not user:
                # Return error if email doesn't exist
                print("[PASSWORD RESET SERVICE] User not found")
                return {
                    "error": "No account found with this email address. Please check and try again."
                }

            # Check if user signed up with Google
            if user.get("auth_provider") == "google":
                print(
                    "[PASSWORD RESET SERVICE] User signed up with Google, cannot reset password"
                )
                return {
                    "error": "This account uses Google Sign-In. Please log in with Google instead."
                }

            user_id = str(user["user_id"])
            username = user["username"]

            # Generate 6-digit code
            code = str(random.randint(100000, 999999))
            print(f"[PASSWORD RESET SERVICE] Generated reset code: {code}")

            # Set expiration time (10 minutes from now)
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
            print(f"[PASSWORD RESET SERVICE] Code expires at: {expires_at}")

            # Store code in database
            success = UserRepository.create_password_reset_code(
                user_id, code, expires_at
            )

            if not success:
                print("[PASSWORD RESET SERVICE] Failed to store reset code in database")
                return {"error": "Failed to create password reset code."}

            # Send email with reset code
            email_sent = EmailService.send_password_reset_email(
                email_address, code, username
            )

            if not email_sent:
                print("[PASSWORD RESET SERVICE] Failed to send email")
                return {"error": "Failed to send password reset email."}

            print("[PASSWORD RESET SERVICE] Password reset email sent successfully")
            return {
                "success": True,
                "user_id": user_id,
                "message": "Password reset code sent to your email.",
            }

        except Exception as e:
            print(f"[PASSWORD RESET SERVICE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    @staticmethod
    def verify_password_reset_code_service(user_id: str, code: str) -> dict:
        """Verify the password reset code."""
        try:
            print(
                f"[VERIFY RESET CODE SERVICE] Verifying code for user: {user_id}, code: {code}"
            )

            is_valid = UserRepository.verify_password_reset_code(user_id, code)

            if not is_valid:
                print("[VERIFY RESET CODE SERVICE] Invalid or expired code")
                return {"error": "Invalid or expired reset code."}

            print("[VERIFY RESET CODE SERVICE] Code verified successfully")
            return {
                "success": True,
                "message": "Code verified successfully!",
            }

        except Exception as e:
            print(f"[VERIFY RESET CODE SERVICE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    @staticmethod
    def reset_password_service(user_id: str, code: str, new_password: str) -> dict:
        """Reset user password after verifying code."""
        try:
            print(f"[RESET PASSWORD SERVICE] Resetting password for user: {user_id}")

            # First, verify the code again
            is_valid = UserRepository.verify_password_reset_code(user_id, code)

            if not is_valid:
                print("[RESET PASSWORD SERVICE] Invalid or expired code")
                return {"error": "Invalid or expired reset code."}

            # Get user info for password validation
            user = UserRepository.get_user_email_and_username(user_id)

            if not user:
                return {"error": "User not found."}

            # Validate new password strength
            validation = PasswordValidator.validate_password(
                new_password,
                user.get("username") or "",
                user.get("email_address") or "",
            )

            if not validation["valid"]:
                print(
                    f"[RESET PASSWORD SERVICE] Password validation failed: {validation['errors']}"
                )
                return {"error": validation["errors"][0]}  # Return first error

            # Update password
            success = UserRepository.update_user_password(user_id, new_password)

            if not success:
                print("[RESET PASSWORD SERVICE] Failed to update password")
                return {"error": "Failed to reset password."}

            print("[RESET PASSWORD SERVICE] Password reset successfully")
            return {
                "success": True,
                "message": "Password reset successfully!",
            }

        except Exception as e:
            print(f"[RESET PASSWORD SERVICE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    @staticmethod
    def resend_password_reset_code_service(user_id: str) -> dict:
        """Resend password reset code to user."""
        try:
            print(f"[RESEND RESET CODE SERVICE] Resending code for user: {user_id}")

            # Get user info
            user = UserRepository.get_user_email_and_username(user_id)

            if not user:
                return {"error": "User not found."}

            email_address = user["email_address"]
            username = user["username"]

            # Generate new code
            code = str(random.randint(100000, 999999))
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

            # Store new code (old one is automatically deleted)
            success = UserRepository.create_password_reset_code(
                user_id, code, expires_at
            )

            if not success:
                return {"error": "Failed to create reset code."}

            # Send email
            email_sent = EmailService.send_password_reset_email(
                email_address, code, username
            )

            if not email_sent:
                return {"error": "Failed to send email."}

            print("[RESEND RESET CODE SERVICE] Code resent successfully")
            return {
                "success": True,
                "message": "A new reset code has been sent to your email.",
            }

        except Exception as e:
            print(f"[RESEND RESET CODE SERVICE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    # ============= CHANGE PASSWORD METHODS (NEW) =============

    @staticmethod
    def request_change_password_code_service(user_id: str) -> dict:
        """Send verification code to user's email for password change."""
        try:
            print(
                f"[CHANGE PASSWORD SERVICE] Starting change password request for user: {user_id}"
            )

            # Get user info
            user = UserRepository.get_user_email_and_username(user_id)

            if not user:
                return {"error": "User not found."}

            # Check if user is Google auth (they can't change password)
            user_full = UserRepository.get_user_by_email_address(user["email_address"])

            if user_full and user_full.get("auth_provider") == "google":
                return {
                    "error": "Cannot change password for Google accounts. Your password is managed by Google."
                }

            email_address = user["email_address"]
            username = user["username"]

            # Generate 6-digit code
            code = str(random.randint(100000, 999999))
            print(f"[CHANGE PASSWORD SERVICE] Generated code: {code}")

            # Set expiration time (10 minutes from now)
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

            # Store code in password_reset_codes table (reusing the same table)
            success = UserRepository.create_password_reset_code(
                user_id, code, expires_at
            )

            if not success:
                return {"error": "Failed to create verification code."}

            # Send email with verification code
            email_sent = EmailService.send_password_reset_email(
                email_address, code, username
            )

            if not email_sent:
                return {"error": "Failed to send verification email."}

            print("[CHANGE PASSWORD SERVICE] Verification email sent successfully")
            return {
                "success": True,
                "message": "Verification code sent to your email.",
            }

        except Exception as e:
            print(f"[CHANGE PASSWORD SERVICE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    @staticmethod
    def verify_change_password_code_service(user_id: str, code: str) -> dict:
        """Verify the change password code."""
        try:
            print(f"[VERIFY CHANGE PASSWORD CODE] Verifying code for user: {user_id}")

            is_valid = UserRepository.verify_password_reset_code(user_id, code)

            if not is_valid:
                print("[VERIFY CHANGE PASSWORD CODE] Invalid or expired code")
                return {"error": "Invalid or expired verification code."}

            print("[VERIFY CHANGE PASSWORD CODE] Code verified successfully")
            return {
                "success": True,
                "message": "Code verified successfully!",
            }

        except Exception as e:
            print(f"[VERIFY CHANGE PASSWORD CODE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    @staticmethod
    def change_password_service(
        user_id: str, code: str, current_password: str, new_password: str
    ) -> dict:
        """Change user password after verifying code and current password."""
        try:
            print(f"[CHANGE PASSWORD SERVICE] Changing password for user: {user_id}")

            # Verify the code
            is_valid = UserRepository.verify_password_reset_code(user_id, code)

            if not is_valid:
                return {"error": "Invalid or expired verification code."}

            # Get user info first
            user_info_temp = UserRepository.get_user_email_and_username(user_id)

            if not user_info_temp:
                return {"error": "User not found."}

            # Verify current password
            user = UserRepository.get_user_by_email_address(
                user_info_temp["email_address"]
            )

            if not user:
                return {"error": "User not found."}

            user["user_id"] = str(user["user_id"])
            user_dataclass = convert_user_dict(user)

            if not user_dataclass.check_password(current_password):
                return {"error": "Current password is incorrect."}

            # Validate new password
            user_info = UserRepository.get_user_email_and_username(user_id)

            if not user_info:
                return {"error": "User not found."}

            validation = PasswordValidator.validate_password(
                new_password,
                user_info.get("username") or "",
                user_info.get("email_address") or "",
            )

            if not validation["valid"]:
                return {"error": validation["errors"][0]}

            # Check if new password is same as current password
            if current_password == new_password:
                return {
                    "error": "New password must be different from current password."
                }

            # Update password
            success = UserRepository.update_user_password(user_id, new_password)

            if not success:
                return {"error": "Failed to change password."}

            print("[CHANGE PASSWORD SERVICE] Password changed successfully")
            return {
                "success": True,
                "message": "Password changed successfully!",
            }

        except Exception as e:
            print(f"[CHANGE PASSWORD SERVICE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    @staticmethod
    def resend_change_password_code_service(user_id: str) -> dict:
        """Resend verification code for password change."""
        try:
            print(f"[RESEND CHANGE PASSWORD CODE] Resending code for user: {user_id}")

            # Get user info
            user = UserRepository.get_user_email_and_username(user_id)

            if not user:
                return {"error": "User not found."}

            email_address = user["email_address"]
            username = user["username"]

            # Generate new code
            code = str(random.randint(100000, 999999))
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

            # Store new code
            success = UserRepository.create_password_reset_code(
                user_id, code, expires_at
            )

            if not success:
                return {"error": "Failed to create verification code."}

            # Send email
            email_sent = EmailService.send_password_reset_email(
                email_address, code, username
            )

            if not email_sent:
                return {"error": "Failed to send email."}

            print("[RESEND CHANGE PASSWORD CODE] Code resent successfully")
            return {
                "success": True,
                "message": "A new verification code has been sent to your email.",
            }

        except Exception as e:
            print(f"[RESEND CHANGE PASSWORD CODE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}
