from flask import Blueprint, Response
from flask_jwt_extended import jwt_required
from .controllers import PurchasesController

purchases_bp = Blueprint("purchases_bp", __name__)


@purchases_bp.route("/create", methods=["POST"])
@jwt_required()
def create_purchase() -> tuple[Response, int]:
    """
    Create a new purchase for a book.

    Expects JSON body containing:
        - book_id: UUID of the book
        - total_buy_cost: Total cost of the purchase
        - meetup_location: Meetup location
        - meetup_date: Meetup date (ISO 8601 string)
        - meetup_time_window: Meetup time window
        - meetup_time:  Exact meetup time (ISO 8601 string)

    Backend defaults:
        - purchase_status: 'pending'
        - all_fees_captured: False
        - owner_confirmed_pickup: False
        - user_confirmed_pickup: False
        - purchase_date: now()

    Response JSON:
        purchase_id: UUID of the created purchase
        messageTitle: Short success message
        message: Detailed success message

    Possible errors:
        400 if required fields are missing
        401 if user not authenticated
        500 if unexpected error occurs
    """
    return PurchasesController.create_purchase_controller()


@purchases_bp.route("/check/<book_id>", methods=["GET"])
@jwt_required()
def check_purchase(book_id: str) -> tuple[Response, int]:
    """
    Check if the current user already purchased a book.

    Args:
        book_id (str): UUID of the book

    Returns JSON:
        exists: True if a pending purchase exists, False otherwise

    Errors:
        401 if user not authenticated
        500 if unexpected error occurs
    """
    return PurchasesController.check_purchase_controller(book_id)
