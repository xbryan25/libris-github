from flask import Blueprint, Response
from .controllers import UserControllers

from flask_jwt_extended import jwt_required

users_bp = Blueprint("users_bp", __name__)


@users_bp.route("/login", methods=["POST"])
def user_login() -> tuple[Response, int]:
    """
    Authenticate a user and start a new session.

    This endpoint expects a JSON body containing 'emailAddress' and 'password'.
    If authentication is successful, the server sets HTTP-only cookies for the
    access and refresh tokens and returns a success message with session details.

    Request body:

        emailAddress: The email address of the user.

        password: The password of the user.

    Response JSON:

        username: The username of the authenticated.

        messageTitle: A short success message.

        message: A friendly message for the user.

        accessTokenExpiresAt: Timestamp (in milliseconds) for when the access token expires.

    Possible errors:

        401 if the credentials are invalid.

        500 if an unexpected error occurs during processing.

    Additional notes:

        HTTP-only cookies for access and refresh tokens are also set.
    """

    return UserControllers.user_login_controller()


@users_bp.route("/logout", methods=["POST"])
def user_logout() -> tuple[Response, int]:
    """
    Log out a user and clear their session.

    This endpoint removes authentication cookies to log out the user. It clears both the access and refresh tokens
    from the client browser.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        messageTitle: A short success message.

        message: A confirmation that the session has been cleared.

    Possible errors:

        500 if an unexpected error occurs during processing.

    Additional notes:

        Both access and refresh cookies are cleared using unset_jwt_cookies().
    """

    return UserControllers.user_logout_controller()


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user() -> tuple[Response, int]:
    """
    Retrieve the currently authenticated user's information.

    This endpoint requires a valid access token (HTTP-only cookie) to identify the user.
    It returns the username associated with the authenticated session.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        username: The username of the currently authenticated user.

    Possible errors:

        401 if the user is not authenticated or the token is missing/invalid.

        500 if an unexpected error occurs during processing.
    """

    return UserControllers.get_current_user_controller()


@users_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_access_token() -> tuple[Response, int]:
    """
    Generate a new access token using a valid refresh token.

    This endpoint requires a valid refresh token (HTTP-only cookie).
    It issues a new access token and updates the access token cookie without requiring the user to log in again.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        accessTokenExpiresAt: Timestamp (in milliseconds) indicating when the new access token will expire.

    Possible errors:

        401 if the refresh token is missing or invalid.

        500 if an unexpected error occurs during processing.
    """

    return UserControllers.refresh_access_token_controller()


@users_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile_info() -> tuple[Response, int]:
    """
    Retrieve the profile information of the currently authenticated user.

    This endpoint requires a valid access token (HTTP-only cookie) to identify the user.
    It returns the user's profile details such as name, date of birth, and contact information.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        A dictionary containing the user's profile information:
            - username
            - accountActivatedAt
            - firstName
            - middleName
            - lastName
            - dateOfBirth
            - phoneNumber
            - address (which includes country, city, barangay, street, postalCode)

    Possible errors:

        401 if the user is not authenticated or the token is missing/invalid.

        500 if an unexpected error occurs during processing.
    """

    return UserControllers.get_profile_info_controller()
