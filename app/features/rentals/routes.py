from flask import Blueprint, Response
from flask_jwt_extended import jwt_required
from .controllers import RentalsController

rentals_bp = Blueprint("rentals_bp", __name__)


@rentals_bp.route("/create", methods=["POST"])
@jwt_required()
def create_rental() -> tuple[Response, int]:
    """
    Create a new rental request for a book.

    This endpoint expects a JSON body containing:
        - book_id: The UUID of the book to rent.
        - total_rent_cost: The total cost of renting the book.
        - rental_duration_days: Number of days for the rental.
        - meetup_time_window: The preferred time window for meetup (e.g., "10:30 AM - 12:00 PM").
        - meetup_location: The meetup location as a string.
        - meetup_date: The preferred date for meetup (ISO 8601 string).

    Defaults handled by backend:
        - rent_status: "pending"
        - reserved_at: current timestamp
        - reservation_expires_at: current timestamp + 1 day
        - all_fees_captured: False

    Response JSON:
        rental_id: The UUID of the created rental.
        messageTitle: Short success message.
        message: Detailed success message.

    Possible errors:
        400 if required fields are missing.
        401 if user is not authenticated.
        500 if an unexpected error occurs during processing.
    """
    return RentalsController.create_rental_controller()


@rentals_bp.route("/check/<book_id>", methods=["GET"])
@jwt_required()
def check_rental(book_id: str) -> tuple[Response, int]:
    """
    Check if the current user already has a pending rental request for a given book.

    Args:
        book_id (str): The UUID of the book.

    Returns JSON:
        exists: True if a pending rental exists, False otherwise.

    Errors:
        401 if user is not authenticated.
        500 if an unexpected error occurs.
    """
    return RentalsController.check_rental_controller(book_id)
