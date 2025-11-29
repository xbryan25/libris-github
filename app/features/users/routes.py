from flask import Blueprint, Response
from .controllers import UserControllers
from flask_jwt_extended import jwt_required

users_bp = Blueprint("users_bp", __name__)


@users_bp.route("/login", methods=["POST"])
def user_login() -> tuple[Response, int]:
    """Authenticate user and start new session."""
    return UserControllers.user_login_controller()


@users_bp.route("/google-login", methods=["POST"])
def user_google_login() -> tuple[Response, int]:
    """
    add later
    """

    return UserControllers.user_google_login_controller()


@users_bp.route("/new-username", methods=["POST"])
def update_username_by_user_id() -> tuple[Response, int]:
    """
    add later
    """

    return UserControllers.update_username_by_user_id_controller()


@users_bp.route("/signup", methods=["POST"])
def user_signup() -> tuple[Response, int]:
    """Register new user account."""
    return UserControllers.user_signup_controller()


@users_bp.route("/send-verification-email", methods=["POST"])
def send_verification_email() -> tuple[Response, int]:
    """Send email verification code to user."""
    return UserControllers.send_verification_email_controller()


@users_bp.route("/verify-email", methods=["POST"])
def verify_email() -> tuple[Response, int]:
    """Verify email with provided code."""
    return UserControllers.verify_email_code_controller()


@users_bp.route("/resend-verification-code", methods=["POST"])
def resend_verification_code() -> tuple[Response, int]:
    """Resend verification code to user email."""
    print("\n[ROUTES] ========== RESEND VERIFICATION CODE ROUTE HIT ==========")
    print("[ROUTES] Routing to resend_verification_code_controller")
    return UserControllers.resend_verification_code_controller()


@users_bp.route("/logout", methods=["POST"])
def user_logout() -> tuple[Response, int]:
    """Log out user and clear session."""
    return UserControllers.user_logout_controller()


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user() -> tuple[Response, int]:
    """Retrieve currently authenticated user information."""
    return UserControllers.get_current_user_controller()


@users_bp.route("/username/<string:user_id>", methods=["GET"])
@jwt_required()
def get_username_from_user_id(user_id: str) -> tuple[Response, int]:
    """Retrieve username of user by their user ID."""
    return UserControllers.get_username_from_user_id_controller(user_id)


@users_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_access_token() -> tuple[Response, int]:
    """Generate new access token using refresh token."""
    return UserControllers.refresh_access_token_controller()


@users_bp.route("/profile/me", methods=["GET"])
@jwt_required()
def get_profile_info() -> tuple[Response, int]:
    """Retrieve authenticated user profile information."""
    return UserControllers.get_profile_info_controller()


@users_bp.route("/profile/<user_id>", methods=["GET"])
@jwt_required()
def get_user_profile_info(user_id: str) -> tuple[Response, int]:
    """Retrieve user profile information by user ID."""
    return UserControllers.get_other_user_profile_controller(user_id)


@users_bp.route("/trust-score-percentile", methods=["GET"])
@jwt_required()
def get_trust_score_percentile() -> tuple[Response, int]:
    """Retrieve trust score percentile for authenticated user."""
    return UserControllers.get_trust_score_comparison_controller()


@users_bp.route("/trust-score-percentile/<string:user_id>", methods=["GET"])
@jwt_required()
def get_other_user_trust_score_percentile(user_id: str) -> tuple[Response, int]:
    """Retrieve trust score percentile for another user by ID."""
    return UserControllers.get_other_user_trust_score_comparison_controller(user_id)


@users_bp.route("/profile/me", methods=["PUT"])
@jwt_required()
def update_user_profile() -> tuple[Response, int]:
    """Update authenticated user profile information."""
    return UserControllers.update_user_profile_controller()


@users_bp.route("/profile/me", methods=["PATCH"])
@jwt_required()
def patch_user_profile() -> tuple[Response, int]:
    """Partially update authenticated user profile."""
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
    """Retrieve book counts for a specific user."""
    return UserControllers.get_library_details_controller(user_id)
