from flask import request, jsonify, make_response, current_app, Response
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    create_refresh_token,
    set_refresh_cookies,
    get_jwt_identity,
    unset_jwt_cookies,
)
import traceback
import uuid
import requests
import datetime

from .services import UserServices
from app.utils.camel_case_converter import dict_keys_to_camel

from app.exceptions.custom_exceptions import EmailInUseByGoogleError


class UserControllers:

    @staticmethod
    def user_login_controller() -> tuple[Response, int]:
        """Generate JWT tokens and set as HTTP-only cookies."""
        user_login_details = request.get_json()

        if user_login_details is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        try:
            user = UserServices.user_login_service(
                user_login_details.get("emailAddress"),
                user_login_details.get("password"),
            )

            if not user:
                return jsonify({"error": "Invalid credentials."}), 401

            access_token = create_access_token(identity=user.user_id)
            refresh_token = create_refresh_token(identity=user.user_id)

            resp = make_response(
                {
                    "userId": user.user_id,
                    "username": user.username,
                    "messageTitle": "Login successful.",
                    "message": "Enjoy your session!",
                    "isEmailVerified": user.is_email_verified,
                }
            )

            set_access_cookies(
                resp, access_token, max_age=current_app.config["COOKIE_MAX_AGE"]
            )

            set_refresh_cookies(
                resp,
                refresh_token,
                max_age=current_app.config["REFRESH_COOKIE_MAX_AGE"],
            )

            return resp, 200

        except EmailInUseByGoogleError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def user_google_login_controller() -> tuple[Response, int]:
        """add later"""

        user_google_login_details = request.get_json()

        if user_google_login_details is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        try:
            data = request.get_json()
            code = data.get("code")

            if not code:
                return jsonify({"error": "Missing Google authorization code"}), 400

            token_resp = requests.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": current_app.config.get("GOOGLE_CLIENT_ID", ""),
                    "client_secret": current_app.config.get("GOOGLE_CLIENT_SECRET", ""),
                    "redirect_uri": "postmessage",
                    "grant_type": "authorization_code",
                },
            )

            token_resp.raise_for_status()
            tokens = token_resp.json()
            id_token = tokens.get("id_token")

            user_info_resp = requests.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
            )
            user_info_resp.raise_for_status()
            user_info = user_info_resp.json()

            email_address = user_info["email"]
            first_name = user_info["given_name"]
            last_name = user_info["family_name"]
            profile_image_url = user_info["picture"]

            user = UserServices.get_user_by_email_address_service(email_address)

            user_id = user["user_id"] if user else None
            auth_provider = user["auth_provider"] if user else None

            if user_id and auth_provider and auth_provider == "local":
                return jsonify({"error": "Email address is already in use."}), 400

            elif not user_id:
                user_id = UserServices.user_google_signup_service(
                    email_address, first_name, last_name, profile_image_url
                )

            username = UserServices.get_username_service(user_id)

            # Generate your JWT access/refresh tokens
            access_token = create_access_token(identity=user_id)
            refresh_token = create_refresh_token(identity=user_id)

            # Set cookies
            resp = make_response(
                {
                    "userId": user_id,
                    "username": username,
                    "messageTitle": "Login successful via Google.",
                    "message": "Enjoy your session!",
                    "isEmailVerified": True,
                }
            )

            if username:
                set_access_cookies(
                    resp, access_token, max_age=current_app.config["COOKIE_MAX_AGE"]
                )
                set_refresh_cookies(
                    resp,
                    refresh_token,
                    max_age=current_app.config["REFRESH_COOKIE_MAX_AGE"],
                )

            return resp, 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_username_by_user_id_controller() -> tuple[Response, int]:
        """test"""

        new_username_details = request.get_json()

        if new_username_details is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        try:
            user_id = new_username_details.get("userId")
            username = new_username_details.get("username")

            if not user_id or not username:
                return (
                    jsonify({"error": "user_id, and username are required."}),
                    400,
                )

            is_username_taken = UserServices.check_if_username_is_taken_service(
                username
            )

            if is_username_taken:
                return (
                    jsonify({"error": f"Username '{username}' is already taken."}),
                    400,
                )

            UserServices.update_username_by_user_id_service(user_id, username)

            access_token = create_access_token(identity=user_id)
            refresh_token = create_refresh_token(identity=user_id)

            resp = make_response(
                {
                    "messageTitle": "Username updated!",
                    "message": "You can now start using Libris. Enjoy your session.",
                }
            )

            set_access_cookies(
                resp, access_token, max_age=current_app.config["COOKIE_MAX_AGE"]
            )
            set_refresh_cookies(
                resp,
                refresh_token,
                max_age=current_app.config["REFRESH_COOKIE_MAX_AGE"],
            )

            return resp, 201

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def user_signup_controller() -> tuple[Response, int]:
        """Create a new user account and initialize wallet."""
        user_signup_details = request.get_json()

        if user_signup_details is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        try:
            username = user_signup_details.get("username")
            email_address = user_signup_details.get("emailAddress")
            password = user_signup_details.get("password")

            if not username or not email_address or not password:
                return (
                    jsonify(
                        {
                            "error": (
                                "Username, email address, and password " "are required."
                            )
                        }
                    ),
                    400,
                )

            result = UserServices.user_signup_service(username, email_address, password)

            if result is None:
                return jsonify({"error": "Signup failed."}), 400

            if "error" in result:
                return jsonify({"error": result["error"]}), 400

            user_id = result.get("user_id")

            resp = make_response(
                {
                    "userId": user_id,
                    "messageTitle": "Account created successfully!",
                    "message": "Welcome to Libris! Login and verify your email to continue.",
                }
            )

            return resp, 201

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def send_verification_email_controller() -> tuple[Response, int]:
        """Send verification email to user."""
        try:
            data = request.get_json()

            user_id = data.get("userId") if data else None

            if not user_id:
                return jsonify({"error": "User ID is required."}), 400

            result = UserServices.send_verification_email_service(user_id)

            if "error" in result:
                return jsonify({"error": result["error"]}), 400

            response = {
                "messageTitle": "Email Sent!",
                "message": "Please check your inbox for the verification code.",
            }

            return jsonify(response), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def verify_email_code_controller() -> tuple[Response, int]:
        """Verify the email verification code."""
        try:

            data = request.get_json()

            user_id = data.get("userId") if data else None
            code = data.get("code") if data else None
            reserved_at = datetime.datetime.now()

            if not user_id or not code:
                error_response = {"error": "User ID and code are required."}
                return jsonify(error_response), 400

            result = UserServices.verify_email_code_service(user_id, code, reserved_at)

            if "error" in result:
                error_response = {"error": result["error"]}
                return jsonify(error_response), 400

            response = {
                "messageTitle": "Email Verified!",
                "message": "Your email has been successfully verified.",
            }

            return jsonify(response), 200

        except Exception as e:
            traceback.print_exc()
            error_response = {"error": str(e)}
            return jsonify(error_response), 500

    @staticmethod
    def resend_verification_code_controller() -> tuple[Response, int]:
        """Resend verification email to user."""
        try:

            data = request.get_json()

            user_id = data.get("userId") if data else None

            if not user_id:

                return jsonify({"error": "User ID is required."}), 400

            result = UserServices.send_verification_email_service(user_id)

            if "error" in result:

                return jsonify({"error": result["error"]}), 400

            response = {
                "messageTitle": "Code Resent!",
                "message": ("A new verification code has been sent to your email."),
            }

            return jsonify(response), 200

        except Exception as e:

            traceback.print_exc()

            return jsonify({"error": str(e)}), 500

    @staticmethod
    def user_logout_controller() -> tuple[Response, int]:
        """Unset both access and refresh tokens."""
        try:
            resp = make_response(
                {
                    "messageTitle": "Logout successful.",
                    "message": "Your session has been cleared.",
                }
            )

            unset_jwt_cookies(resp)

            return resp, 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_current_user_controller() -> tuple[Response, int]:
        """Retrieve the currently authenticated user's username."""
        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401

            username = UserServices.get_username_service(user_id)

            is_email_verified = UserServices.get_is_email_verified_service(user_id)

            return (
                jsonify(
                    {
                        "username": username,
                        "userId": user_id,
                        "isEmailVerified": is_email_verified,
                    }
                ),
                200,
            )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_username_from_user_id_controller(
        user_id: str,
    ) -> tuple[Response, int]:
        """Retrieve the username of a user by their user ID."""
        try:
            username = UserServices.get_username_service(user_id)

            return jsonify({"username": username}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def refresh_access_token_controller() -> tuple[Response, int]:
        """Generate a new access token using a refresh token."""
        try:
            identity = get_jwt_identity()

            new_access_token = create_access_token(identity=identity)

            resp = make_response({"message": "access_token refreshed successfully."})

            set_access_cookies(
                resp,
                new_access_token,
                max_age=current_app.config["COOKIE_MAX_AGE"],
            )

            return resp, 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_profile_info_controller() -> tuple[Response, int]:
        """Retrieve the authenticated user's profile."""
        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401

            profile_info = UserServices.get_profile_info_service(user_id)

            if profile_info is None:
                return jsonify({"message": "User profile not found."}), 404

            profile_info["address"] = {
                "country": profile_info.pop("country", None),
                "city": profile_info.pop("city", None),
                "barangay": profile_info.pop("barangay", None),
                "street": profile_info.pop("street", None),
                "postal_code": profile_info.pop("postal_code", None),
                "latitude": profile_info.pop("latitude", None),
                "longitude": profile_info.pop("longitude", None),
            }

            return jsonify(profile_info), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_other_user_profile_controller(
        user_id: str,
    ) -> tuple[Response, int]:
        """Retrieve another user's profile by user_id."""
        try:
            try:
                uuid.UUID(user_id)
            except ValueError:
                return jsonify({"message": "Invalid user ID format."}), 400

            profile_info = UserServices.get_profile_info_service(user_id)

            if profile_info is None:
                return jsonify({"message": "User not found."}), 404

            profile_info["address"] = {
                "country": profile_info.pop("country", None),
                "city": profile_info.pop("city", None),
                "barangay": profile_info.pop("barangay", None),
                "street": profile_info.pop("street", None),
                "postal_code": profile_info.pop("postal_code", None),
                "latitude": profile_info.pop("latitude", None),
                "longitude": profile_info.pop("longitude", None),
            }

            return jsonify(profile_info), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_trust_score_comparison_controller() -> tuple[Response, int]:
        """Retrieve trust score percentile for authenticated user."""
        try:
            user_id = str(get_jwt_identity())

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401

            comparison_stats = UserServices.get_trust_score_comparison_service(user_id)

            if not comparison_stats:
                return (
                    jsonify({"message": "Trust score statistics not available."}),
                    404,
                )

            return jsonify(comparison_stats), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_user_profile_controller() -> tuple[Response, int]:
        """Update authenticated user's profile information."""
        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401

            profile_data = request.get_json()

            if not profile_data:
                return jsonify({"message": "No data provided"}), 400

            profile_success = UserServices.update_user_profile_service(
                user_id, profile_data
            )

            address_success = True

            if "address" in profile_data:
                address_success = UserServices.update_user_address_service(
                    user_id, profile_data["address"]
                )

            if profile_success and address_success:
                return (
                    jsonify({"message": "Profile updated successfully"}),
                    200,
                )

            return jsonify({"message": "Failed to update profile"}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_other_user_trust_score_comparison_controller(
        user_id: str,
    ) -> tuple[Response, int]:
        """Retrieve trust score percentile for another user."""
        try:
            comparison_stats = UserServices.get_trust_score_comparison_service(user_id)

            if not comparison_stats:
                return (
                    jsonify({"message": "Trust score statistics not available."}),
                    404,
                )

            return jsonify(comparison_stats), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def patch_user_profile_controller() -> tuple[Response, int]:
        """Partially update authenticated user's profile."""
        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401

            profile_data = request.get_json()

            if not profile_data:
                return jsonify({"message": "No data provided"}), 400

            profile_success = True

            address_success = True

            if "profile_image_url" in profile_data or any(
                k in profile_data
                for k in [
                    "first_name",
                    "middle_name",
                    "last_name",
                    "date_of_birth",
                    "phone_number",
                ]
            ):
                profile_success = UserServices.update_user_profile_service(
                    user_id, profile_data
                )

            if "address" in profile_data:
                address_success = UserServices.update_user_address_service(
                    user_id, profile_data["address"]
                )

            if profile_success and address_success:
                return (
                    jsonify({"message": "Profile updated successfully"}),
                    200,
                )

            return jsonify({"message": "Failed to update profile"}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_personal_info_controller() -> tuple[Response, int]:
        """Update only the personal information (not address) of the authenticated user."""

        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401

            profile_data = request.get_json()

            if not profile_data:
                return jsonify({"message": "No data provided"}), 400

            profile_success = UserServices.update_user_profile_service(
                user_id, profile_data
            )

            if profile_success:
                return (
                    jsonify({"message": "Personal information updated successfully"}),
                    200,
                )
            else:
                return (
                    jsonify({"message": "Failed to update personal information"}),
                    500,
                )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_address_controller() -> tuple[Response, int]:
        """Update only the address information of the authenticated user."""

        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401

            address_data = request.get_json()

            if not address_data:
                return jsonify({"message": "No data provided"}), 400

            address_success = UserServices.update_user_address_service(
                user_id, address_data
            )

            if address_success:
                return jsonify({"message": "Address updated successfully"}), 200
            else:
                return jsonify({"message": "Failed to update address"}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_library_details_controller(user_id) -> tuple[Response, int]:
        """Retrieve the number of owned, rented, and bought books for a specific user."""

        try:
            library_details = UserServices.get_library_details_service(user_id)

            return (
                jsonify(dict_keys_to_camel(library_details or {})),
                200,
            )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
