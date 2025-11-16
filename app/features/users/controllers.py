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

from .services import UserServices

from app.utils.camel_case_converter import dict_keys_to_camel


class UserControllers:

    @staticmethod
    def user_login_controller() -> tuple[Response, int]:
        """Generate JWT access and refresh tokens, and set them as HTTP-only cookies after validating user credentials."""

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
                    "username": user.username,
                    "messageTitle": "Login successful.",
                    "message": "Enjoy your session!",
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

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def user_signup_controller() -> tuple[Response, int]:
        """Create a new user account and initialize their wallet."""

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
                        {"error": "Username, email address, and password are required."}
                    ),
                    400,
                )

            result = UserServices.user_signup_service(username, email_address, password)

            if result is None:
                return jsonify({"error": "Signup failed."}), 400

            if "error" in result:
                return jsonify({"error": result["error"]}), 400

            resp = make_response(
                {
                    "messageTitle": "Account created successfully!",
                    "message": "Welcome to Libris! Please log in to continue.",
                }
            )

            return resp, 201

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def user_logout_controller() -> tuple[Response, int]:
        """Unsets both access and refresh tokens."""

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
        "Retrieve the currently authenticated user's username."

        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401

            username = UserServices.get_username_service(user_id)

            return jsonify({"username": username, "userId": user_id}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_username_from_user_id_controller(user_id) -> tuple[Response, int]:
        "Retrieve the username of a user by their user ID."

        try:
            username = UserServices.get_username_service(user_id)

            return jsonify({"username": username}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def refresh_access_token_controller() -> tuple[Response, int]:
        "Generate a new access token using a valid refresh token."

        try:
            identity = get_jwt_identity()

            new_access_token = create_access_token(identity=identity)

            resp = make_response({"message": "access_token refreshed successfully."})

            set_access_cookies(
                resp, new_access_token, max_age=current_app.config["COOKIE_MAX_AGE"]
            )

            return resp, 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_profile_info_controller() -> tuple[Response, int]:
        "Retrieve the full profile (personal + address) of the authenticated user."

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
            }

            return jsonify(profile_info), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_other_user_profile_controller(user_id: str) -> tuple[Response, int]:
        "Retrieve the full profile (personal + address) of another user by user_id."

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
            }

            return jsonify(profile_info), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_trust_score_comparison_controller() -> tuple[Response, int]:
        """Retrieve trust score percentile for the authenticated user (UUID)."""

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
        """Update the authenticated user's profile information."""

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
                return jsonify({"message": "Profile updated successfully"}), 200
            else:
                return jsonify({"message": "Failed to update profile"}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_other_user_trust_score_comparison_controller(
        user_id: str,
    ) -> tuple[Response, int]:
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
        """Partially update the authenticated user's profile."""

        try:
            user_id = get_jwt_identity()
            # print("JWT user_id:", user_id)  # <-- add this

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401

            profile_data = request.get_json()
            # print("PATCH request body:", profile_data)  # <-- add this

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
                return jsonify({"message": "Profile updated successfully"}), 200
            else:
                return jsonify({"message": "Failed to update profile"}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_library_details_controller(user_id) -> tuple[Response, int]:
        """Retrieve the number of owned, rented, and bought books for a specific user."""

        try:
            library_details = UserServices.get_library_details_service(user_id)

            return jsonify(dict_keys_to_camel(library_details or {})), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
