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

from .services import UserServices

from datetime import datetime, timedelta, timezone


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

            expires_at = (
                datetime.now(timezone.utc)
                + timedelta(seconds=current_app.config["COOKIE_MAX_AGE"])
            ).timestamp() * 1000

            resp = make_response(
                {
                    "username": user.username,
                    "messageTitle": "Login successful.",
                    "message": "Enjoy your session!",
                    "accessTokenExpiresAt": expires_at,
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
    def user_logout_controller() -> tuple[Response, int]:
        """Unsets both access and refresh tokens."""

        try:
            resp = make_response(
                {
                    "messageTitle": "Logout successful.",
                    "message": "Your session has been cleared.",
                }
            )

            # Clears both access and refresh cookies
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

            return jsonify({"username": username}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def refresh_access_token_controller() -> tuple[Response, int]:
        "Generate a new access token using a valid refresh token."

        try:
            # Get user ID from the refresh token
            identity = get_jwt_identity()

            new_access_token = create_access_token(identity=identity)

            expires_at = (
                datetime.now(timezone.utc)
                + timedelta(seconds=current_app.config["COOKIE_MAX_AGE"])
            ).timestamp() * 1000

            resp = make_response({"accessTokenExpiresAt": expires_at})

            set_access_cookies(
                resp, new_access_token, max_age=current_app.config["COOKIE_MAX_AGE"]
            )

            return resp, 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
