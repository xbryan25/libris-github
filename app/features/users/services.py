from .repository import UserRepository
from typing import Any
from app.common.dataclasses import User
from app.utils import convert_user_dict
import random
from datetime import datetime, timedelta, timezone
from app.services.email_service import EmailService


class UserServices:

    @staticmethod
    def user_login_service(email_address: str, password: str) -> User | None:
        """Authenticate user with email address and password."""
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
        """Create new user account and initialize wallet."""
        print(
            f"[SIGNUP SERVICE] Starting signup for username: {username}, "
            f"email: {email_address}"
        )

        existing_user_by_email = UserRepository.get_user_by_email_address(email_address)
        if existing_user_by_email:
            print("[SIGNUP SERVICE] Email already exists!")
            return {"error": "Email address already exists.", "type": "email"}

        existing_user_by_username = UserRepository.get_user_by_username(username)
        if existing_user_by_username:
            print("[SIGNUP SERVICE] Username already exists!")
            return {"error": "Username already exists.", "type": "username"}

        user_id = UserRepository.create_user(username, email_address, password)
        print(f"[SIGNUP SERVICE] User created with ID: {user_id}")

        UserRepository.initialize_wallet(user_id)
        print("[SIGNUP SERVICE] Wallet initialized")

        # Generate and send verification code
        print("[SIGNUP SERVICE] Generating verification code...")
        code = UserServices.generate_verification_code()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

        success = UserRepository.create_verification_code(user_id, code, expires_at)
        if not success:
            print("[SIGNUP SERVICE] Failed to store verification code " "in database!")
            return {"error": "Failed to create verification code."}

        print("[SIGNUP SERVICE] Verification code stored. Sending email...")
        email_sent = EmailService.send_verification_email(email_address, code, username)

        if not email_sent:
            print("[SIGNUP SERVICE] Failed to send verification email!")
            return {"error": "Failed to send verification email."}

        print("[SIGNUP SERVICE] Success! Email sent.")
        return {"success": True, "user_id": user_id}

    @staticmethod
    def generate_verification_code() -> str:
        """Generate random 6-digit verification code."""
        code = str(random.randint(100000, 999999))
        print(f"[SERVICE] Generated verification code: {code}")
        return code

    @staticmethod
    def send_verification_email_service(user_id: str) -> dict:
        """Generate verification code, store it, and send email."""
        try:
            print(
                "[VERIFY SERVICE] Starting email verification for " f"user: {user_id}"
            )

            user_data = UserRepository.get_user_email_and_username(user_id)
            print(f"[VERIFY SERVICE] Got user data: {user_data}")

            if not user_data:
                print("[VERIFY SERVICE] User not found!")
                return {"error": "User not found."}

            # Generate new code
            code = UserServices.generate_verification_code()
            print(f"[VERIFY SERVICE] Generated code: {code}")

            # Set expiration time (10 minutes from now)
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
            print(f"[VERIFY SERVICE] Code expires at: {expires_at}")

            # Store code in database (old codes are deleted automatically)
            success = UserRepository.create_verification_code(user_id, code, expires_at)
            print(f"[VERIFY SERVICE] Code stored in DB: {success}")

            if not success:
                print("[VERIFY SERVICE] Failed to store code in database!")
                return {"error": "Failed to create verification code."}

            # Send email with the new code
            print(
                f"[VERIFY SERVICE] Calling "
                f"EmailService.send_verification_email to "
                f"{user_data['email_address']}..."
            )
            email_sent = EmailService.send_verification_email(
                user_data["email_address"], code, user_data["username"]
            )

            print(f"[VERIFY SERVICE] Email sent result: {email_sent}")

            if not email_sent:
                print("[VERIFY SERVICE] Email sending failed!")
                return {"error": "Failed to send verification email."}

            print("[VERIFY SERVICE] Success! Email sent.")
            return {
                "success": True,
                "message": "Verification email sent successfully.",
            }

        except Exception as e:
            print(f"[VERIFY SERVICE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    @staticmethod
    def verify_email_code_service(user_id: str, code: str) -> dict:
        """Verify the email verification code."""
        try:
            print(
                f"[VERIFY CODE SERVICE] Verifying code for user: "
                f"{user_id}, code: {code}"
            )

            if UserRepository.is_email_verified(user_id):
                print("[VERIFY CODE SERVICE] Email already verified!")
                return {"error": "Email is already verified."}

            is_valid = UserRepository.verify_email_code(user_id, code)
            print(f"[VERIFY CODE SERVICE] Code valid: {is_valid}")

            if not is_valid:
                print("[VERIFY CODE SERVICE] Invalid or expired code!")
                return {"error": "Invalid or expired verification code."}

            success = UserRepository.mark_email_as_verified(user_id)
            print(f"[VERIFY CODE SERVICE] Email marked as verified: {success}")

            if not success:
                print("[VERIFY CODE SERVICE] Failed to mark email as verified!")
                return {"error": "Failed to verify email."}

            print("[VERIFY CODE SERVICE] Success! Email verified.")
            return {
                "success": True,
                "message": "Email verified successfully!",
            }

        except Exception as e:
            print(f"[VERIFY CODE SERVICE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"error": "An unexpected error occurred."}

    @staticmethod
    def get_username_service(user_id) -> str | None:
        """Get the username of a user using the user_id."""
        username_dict = UserRepository.get_username(user_id)
        if username_dict is None:
            return None
        return username_dict["username"]

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

        except Exception as e:
            print(f"Error updating user profile: {e}")
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
