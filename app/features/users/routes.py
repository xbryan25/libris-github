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


@users_bp.route("/signup", methods=["POST"])
def user_signup() -> tuple[Response, int]:
    """
    Register a new user account.

    This endpoint expects a JSON body containing 'username', 'emailAddress', and 'password'.
    If registration is successful, the server creates a new user account and initializes
    a readit wallet with a balance of 0.

    Request body:

        username: The desired username for the new account.

        emailAddress: The email address of the user.

        password: The password for the new account.

    Response JSON:

        messageTitle: A short success message.

        message: A friendly message for the user.

    Possible errors:

        400 if the email already exists or validation fails.

        500 if an unexpected error occurs during processing.

    Additional notes:

        User wallet is initialized with balance 0.
    """

    return UserControllers.user_signup_controller()


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


@users_bp.route("/username/<string:user_id>", methods=["GET"])
@jwt_required()
def get_username_from_user_id(user_id: str) -> tuple[Response, int]:
    """
    Retrieve the username of a user by their user ID.

    It returns the user's username.

    Request parameters:

        user_id (str): The unique identifier of the user whose username is to be retrieved.

    Response JSON:

        username: The username of the user whose username is to be retrieved.

    Possible errors:

        401 if the user is not authenticated or the token is missing/invalid.

        404 if no user is found with the provided user ID.

        500 if an unexpected error occurs during processing.
    """
    return UserControllers.get_username_from_user_id_controller(user_id)


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


@users_bp.route("/profile/me", methods=["GET"])
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


@users_bp.route("/profile/<user_id>", methods=["GET"])
@jwt_required()
def get_user_profile_info(user_id: str) -> tuple[Response, int]:
    """
    Retrieve the profile information of a user by their user ID.

    It returns the user's profile details such as name, date of birth, and contact information.

    Request parameters:

        user_id (str): The unique identifier of the user whose profile information is to be retrieved.

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

        404 if no user is found with the provided user ID.

        500 if an unexpected error occurs during processing.
    """

    return UserControllers.get_other_user_profile_controller(user_id)


@users_bp.route("/trust-score-percentile", methods=["GET"])
@jwt_required()
def get_trust_score_percentile() -> tuple[Response, int]:
    """
    Retrieve trust score percentile for the authenticated user.

    Returns JSON:
        - user_id: ID of the authenticated user
        - trust_score_percentile: User's trust score percentile among all users
        - is_above_average: True if percentile > 50, else False

    Possible errors:
        401 if not authenticated
        404 if statistics not available
        500 for unexpected errors
    """
    return UserControllers.get_trust_score_comparison_controller()


@users_bp.route("/trust-score-percentile/<string:user_id>", methods=["GET"])
@jwt_required()
def get_other_user_trust_score_percentile(user_id: str) -> tuple[Response, int]:
    """
    Retrieve trust score percentile for another user by ID.

    Args:
        user_id (str): ID of the user to query

    Returns JSON:
        - user_id: ID of the specified user
        - trust_score_percentile: User's trust score percentile among all users
        - is_above_average: True if percentile > 50, else False

    Possible errors:
        401 if not authenticated
        404 if statistics not available
        500 for unexpected errors
    """
    return UserControllers.get_other_user_trust_score_comparison_controller(user_id)


@users_bp.route("/profile/me", methods=["PUT"])
@jwt_required()
def update_user_profile() -> tuple[Response, int]:
    """
    Update the authenticated user's profile information.

    This endpoint requires a valid access token (HTTP-only cookie) to identify the user.
    It allows updating personal information and address details.

    Request body:

        A JSON object containing the fields to update:
            - first_name (optional): User's first name
            - middle_name (optional): User's middle name
            - last_name (optional): User's last name
            - date_of_birth (optional): User's date of birth
            - phone_number (optional): User's phone number
            - address (optional): Object containing address fields:
                - country (optional): User's country
                - city (optional): User's city
                - barangay (optional): User's barangay
                - street (optional): User's street
                - postal_code (optional): User's postal code

    Response JSON:

        message: Success or error message

    Possible errors:

        401 if the user is not authenticated or the token is missing/invalid.

        400 if no data is provided.

        500 if an unexpected error occurs during processing.
    """

    return UserControllers.update_user_profile_controller()


@users_bp.route("/profile/me", methods=["PATCH"])
@jwt_required()
def patch_user_profile() -> tuple[Response, int]:
    """
    Partially update authenticated user's profile. Only fields provided in the
    JSON body will be updated; other fields remain unchanged.
    """
    return UserControllers.patch_user_profile_controller()


@users_bp.route("/profile/me/personal", methods=["PUT"])
@jwt_required()
def update_personal_info() -> tuple[Response, int]:
    """
    Update only the personal information (not address) of the authenticated user.

    This endpoint requires a valid access token (HTTP-only cookie) to identify the user.
    It allows updating personal information fields only.

    Request body:
        A JSON object containing the fields to update:
            - first_name (optional): User's first name
            - middle_name (optional): User's middle name
            - last_name (optional): User's last name
            - date_of_birth (optional): User's date of birth
            - phone_number (optional): User's phone number

    Response JSON:
        message: Success or error message

    Possible errors:
        401 if the user is not authenticated or the token is missing/invalid.
        400 if no data is provided.
        500 if an unexpected error occurs during processing.
    """
    return UserControllers.update_personal_info_controller()


@users_bp.route("/profile/me/address", methods=["PUT"])
@jwt_required()
def update_address() -> tuple[Response, int]:
    """
    Update only the address information of the authenticated user.

    This endpoint requires a valid access token (HTTP-only cookie) to identify the user.
    It allows updating address fields only.

    Request body:
        A JSON object containing address fields to update:
            - country (optional): User's country
            - city (optional): User's city
            - barangay (optional): User's barangay
            - street (optional): User's street
            - postal_code (optional): User's postal code

    Response JSON:
        message: Success or error message

    Possible errors:
        401 if the user is not authenticated or the token is missing/invalid.
        400 if no data is provided.
        500 if an unexpected error occurs during processing.
    """
    return UserControllers.update_address_controller()


@users_bp.route("/library-details/<string:user_id>", methods=["GET"])
@jwt_required()
def get_library_details(user_id: str) -> tuple[Response, int]:
    """
    Retrieve the number of owned, rented, and bought books for a specific user.

    Request parameters:
        user_id (str): The unique identifier of the user whose book counts are to be retrieved.

    Response JSON:
        owned_count (int): The total number of books owned by the user.
        rented_count (int):The total number of books the user has rented (past and present).
        bought_count (int): The total number of books purchased by the user.

    Possible Errors:
        401 if the user is not authenticated or the token is missing/invalid.

        404 if no user found with the provided user ID.

        500 if an unexpected error occurred during processing.
    """
    return UserControllers.get_library_details_controller(user_id)
