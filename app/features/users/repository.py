from app.db.queries.common import CommonQueries
from app.db.queries.user_queries import UserQueries
from flask import current_app
from werkzeug.security import generate_password_hash
from datetime import datetime


class UserRepository:
    @staticmethod
    def get_user_by_email_address(email_address: str) -> dict[str, str] | None:
        """Retrieve user record by email address."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            CommonQueries.GET_BY_SPECIFIC_COLUMN.format(
                table="users", column="email_address"
            ),
            (email_address,),
        )

    @staticmethod
    def get_user_by_username(username: str) -> dict[str, str] | None:
        """Retrieve user record by username."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            CommonQueries.GET_BY_SPECIFIC_COLUMN.format(
                table="users", column="username"
            ),
            (username,),
        )

    @staticmethod
    def update_username_by_user_id(user_id: str, username: str) -> None:
        """
        add later
        """
        db = current_app.extensions["db"]
        return db.execute_query(
            CommonQueries.UPDATE_BY_ID.format(
                table="users", set_clause="username = %s", pk="user_id"
            ),
            (username, user_id),
        )

    @staticmethod
    def get_user_info(user_id: str) -> dict[str, str | bool] | None:
        """Retrieve username, email verification status, and auth provider by user_id."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            UserQueries.GET_USER_INFO,
            (user_id,),
        )

    @staticmethod
    def get_username(user_id: str) -> dict[str, str] | None:
        """Retrieve username by user_id."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            CommonQueries.GET_COLUMN_BY_FIELD.format(
                column="username", table="users", field="user_id"
            ),
            (user_id,),
        )

    @staticmethod
    def check_if_username_is_taken(username: str) -> dict[str, bool]:
        """
        add later
        """
        db = current_app.extensions["db"]
        return db.fetch_one(
            CommonQueries.CHECK_IF_EXISTS.format(table="users", column="username"),
            (username,),
        )

    @staticmethod
    def create_user(username: str, email_address: str, password: str) -> str:
        """Create new user in database."""
        db = current_app.extensions["db"]
        hashed_password = generate_password_hash(password)
        result = db.fetch_one(
            "INSERT INTO users (username, email_address, password_hash, "
            "trust_score) VALUES (%s, %s, %s, 500) RETURNING user_id",
            (username, email_address, hashed_password),
        )
        return str(result["user_id"])

    @staticmethod
    def create_user_from_google(
        email_address: str,
        first_name: str,
        last_name: str,
        profile_image_url: str | None,
    ) -> str:
        """
        add later
        """
        db = current_app.extensions["db"]
        result = db.fetch_one(
            """INSERT INTO users
            (email_address, first_name, last_name, profile_image_url, auth_provider, is_email_verified, trust_score)
            VALUES (%s, %s, %s, %s, %s, %s, 500) RETURNING user_id""",
            (email_address, first_name, last_name, profile_image_url, "google", True),
        )
        return str(result["user_id"])

    @staticmethod
    def initialize_wallet(user_id: str) -> None:
        """Initialize wallet for new user with balance of 0."""
        db = current_app.extensions["db"]
        db.execute_query(
            "INSERT INTO readits_wallets (user_id, balance) VALUES (%s, %s)",
            (user_id, 0),
        )

    @staticmethod
    def create_verification_code(user_id: str, code: str, expires_at: datetime) -> bool:
        """Store email verification code in database."""
        db = current_app.extensions["db"]
        try:
            # Delete old codes for this user first
            db.execute_query(
                "DELETE FROM email_verifications WHERE user_id = %s",
                (user_id,),
            )
            # Insert new code
            db.execute_query(
                "INSERT INTO email_verifications "
                "(user_id, code, expires_at) VALUES (%s, %s, %s)",
                (user_id, code, expires_at),
            )
            return True

        except Exception:
            import traceback

            traceback.print_exc()
            return False

    @staticmethod
    def verify_email_code(user_id: str, code: str) -> bool:
        """Verify if code is valid and not expired."""
        db = current_app.extensions["db"]

        try:
            # Query for matching code that hasn't expired
            result = db.fetch_one(
                "SELECT * FROM email_verifications "
                "WHERE user_id = %s AND code = %s AND expires_at > NOW()",
                (user_id, code),
            )

            if result is None:

                return False

            return True

        except Exception:

            import traceback

            traceback.print_exc()

            return False

    @staticmethod
    def mark_email_as_verified(user_id: str) -> bool:
        """Mark user email as verified and delete verification code."""
        db = current_app.extensions["db"]
        try:
            db.execute_query(
                "UPDATE users SET is_email_verified = TRUE " "WHERE user_id = %s",
                (user_id,),
            )
            db.execute_query(
                "DELETE FROM email_verifications WHERE user_id = %s",
                (user_id,),
            )

            return True

        except Exception:

            import traceback

            traceback.print_exc()
            return False

    @staticmethod
    def update_account_activated_at(
        user_id: str, account_activated_at: datetime
    ) -> None:
        """Update account_activated_at column of a user."""
        db = current_app.extensions["db"]

        db.execute_query(
            CommonQueries.UPDATE_BY_ID.format(
                table="users", set_clause="account_activated_at = %s", pk="user_id"
            ),
            (account_activated_at, user_id),
        )

    @staticmethod
    def get_user_email_and_username(user_id: str) -> dict | None:
        """Get user email and username for verification email."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            "SELECT email_address, username FROM users WHERE user_id = %s",
            (user_id,),
        )

    @staticmethod
    def is_email_verified(user_id: str) -> bool:
        """Check if user email is already verified."""
        db = current_app.extensions["db"]
        result = db.fetch_one(
            "SELECT is_email_verified FROM users WHERE user_id = %s",
            (user_id,),
        )
        return result and result.get("is_email_verified", False)

    @staticmethod
    def get_profile_info(user_id: str) -> dict[str, str] | None:
        """Retrieve profile information by user_id."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            UserQueries.GET_PROFILE_INFO,
            (user_id,),
        )

    @staticmethod
    def get_trust_score_percentile(user_id: str) -> dict[str, float] | None:
        """Retrieve trust score percentile for specific user."""
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
        """Update user profile information."""
        db = current_app.extensions["db"]

        date_of_birth = profile_data.get("date_of_birth") or None

        try:
            db.execute_query(
                UserQueries.UPDATE_USER_PROFILE,
                (
                    profile_data.get("first_name"),
                    profile_data.get("middle_name"),
                    profile_data.get("last_name"),
                    date_of_birth,
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
        """Update user address information."""
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
                        address_data.get("latitude"),
                        address_data.get("longitude"),
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
                        address_data.get("latitude"),
                        address_data.get("longitude"),
                        user_id,
                    ),
                )

            return True

        except Exception:
            return False

    @staticmethod
    def get_user_address(user_id: str) -> dict[str, str] | None:
        """Retrieve address information by user_id."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            UserQueries.GET_USER_ADDRESS,
            (user_id,),
        )

    @staticmethod
    def get_user_profile(user_id: str) -> dict[str, str] | None:
        """Retrieve profile information by user_id."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            UserQueries.GET_USER_PROFILE,
            (user_id,),
        )

    @staticmethod
    def get_library_details(user_id: str) -> dict[str, int] | None:
        """Retrieve book counts for specific user."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            UserQueries.GET_LIBRARY_DETAILS,
            (user_id, user_id, user_id),
        )

    # PASSWORD RESET METHODS (NEW)

    @staticmethod
    def create_password_reset_code(
        user_id: str, code: str, expires_at: datetime
    ) -> bool:
        """Store password reset code in database."""
        db = current_app.extensions["db"]
        try:
            print(f"[REPOSITORY] Deleting old password reset codes for user: {user_id}")
            # Delete old codes for this user first
            db.execute_query(
                "DELETE FROM password_reset_codes WHERE user_id = %s",
                (user_id,),
            )
            print("[REPOSITORY] Old codes deleted")

            print(
                f"[REPOSITORY] Inserting new password reset code: {code}, "
                f"expires at: {expires_at}"
            )
            # Insert new code
            db.execute_query(
                "INSERT INTO password_reset_codes "
                "(user_id, code, expires_at) VALUES (%s, %s, %s)",
                (user_id, code, expires_at),
            )
            print("[REPOSITORY] New password reset code inserted successfully")
            return True

        except Exception as e:
            print(f"[REPOSITORY] Error creating password reset code: {e}")
            import traceback

            traceback.print_exc()
            return False

    @staticmethod
    def verify_password_reset_code(user_id: str, code: str) -> bool:
        """Verify if password reset code is valid and not expired."""
        db = current_app.extensions["db"]
        print("\n[REPOSITORY] ========== VERIFY PASSWORD RESET CODE ==========")
        print(f"[REPOSITORY] User ID: {user_id}")
        print(f"[REPOSITORY] Code to verify: {code}")

        try:
            # Query for matching code that hasn't expired
            result = db.fetch_one(
                "SELECT * FROM password_reset_codes "
                "WHERE user_id = %s AND code = %s AND expires_at > NOW()",
                (user_id, code),
            )

            print(f"[REPOSITORY] Query result: {result}")

            if result is None:
                print(
                    "[REPOSITORY] Code verification FAILED - "
                    "no matching code or code expired"
                )
                print(
                    "[REPOSITORY] ========== VERIFY PASSWORD RESET CODE COMPLETE "
                    "==========\n"
                )
                return False

            print("[REPOSITORY] Password reset code verification SUCCESSFUL")
            print(
                "[REPOSITORY] ========== VERIFY PASSWORD RESET CODE COMPLETE "
                "==========\n"
            )
            return True

        except Exception as e:
            print(f"[REPOSITORY] ERROR during code verification: {e}")
            import traceback

            traceback.print_exc()
            print(
                "[REPOSITORY] ========== VERIFY PASSWORD RESET CODE COMPLETE "
                "==========\n"
            )
            return False

    @staticmethod
    def update_user_password(user_id: str, new_password: str) -> bool:
        """Update user's password with new hashed password."""
        db = current_app.extensions["db"]
        try:
            print(f"[REPOSITORY] Updating password for user: {user_id}")
            hashed_password = generate_password_hash(new_password)

            db.execute_query(
                "UPDATE users SET password_hash = %s WHERE user_id = %s",
                (hashed_password, user_id),
            )
            print("[REPOSITORY] Password updated successfully")

            # Delete all password reset codes for this user after successful reset
            print(f"[REPOSITORY] Deleting password reset codes for user: {user_id}")
            db.execute_query(
                "DELETE FROM password_reset_codes WHERE user_id = %s",
                (user_id,),
            )
            print("[REPOSITORY] Password reset codes deleted")

            return True

        except Exception as e:
            print(f"[REPOSITORY] Error updating password: {e}")
            import traceback

            traceback.print_exc()
            return False

    @staticmethod
    def get_user_by_email_for_reset(email_address: str) -> dict | None:
        """Get user info for password reset (exclude Google auth users)."""
        db = current_app.extensions["db"]
        try:
            result = db.fetch_one(
                "SELECT user_id, email_address, username, auth_provider "
                "FROM users WHERE email_address = %s",
                (email_address,),
            )
            return result
        except Exception as e:
            print(f"[REPOSITORY] Error fetching user by email: {e}")
            return None
