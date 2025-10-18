from flask import Blueprint, Response
from .controllers import UserControllers

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
