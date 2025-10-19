from flask import Blueprint, Response
from .controllers import DashboardController
from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
def get_dashboard_summary() -> tuple[Response, int]:
    """
    Retrieve the general dashboard summary for the currently authenticated user.

    This endpoint requires a valid access token to identify the user.
    Returns counts for books borrowed, currently lending, currently renting,
    books sold, books bought, and total earnings.

    Request body:
        None. User is identified via JWT access token.

    Response JSON:
        books_borrowed: int
        currently_lending: int
        currently_renting: int
        books_sold: int
        books_bought: int
        total_earnings: int

    Possible errors:
        401 if the user is not authenticated.
        500 if an unexpected error occurs.
    """
    return DashboardController.get_summary_controller()
