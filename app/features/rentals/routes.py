from flask import Blueprint, Response
from flask import jsonify
from flask_jwt_extended import jwt_required
from .controllers import RentalsController

rentals_bp = Blueprint("rentals_bp", __name__)


@rentals_bp.route("/my-rentals", methods=["GET"])
@jwt_required()
def get_my_rentals() -> tuple[Response, int]:
    """
    Retrieve all active rentals for the authenticated user.

    This endpoint returns rentals with statuses:
    'pending', 'approved', 'awaiting_pickup_confirmation', 'ongoing', 'awaiting_return_confirmation'

    Response JSON:
        [
            {
                "rental_id": str,
                "rent_status": str,
                "book_id": str,
                "title": str,
                "author": str,
                "image": str,
                "from": str,
                "all_fees_captured": bool,
                "reserved_at": str,
                "reservation_expires_at": str,
                "rental_duration_days": int,
                "meetup_location": str,
                "meetup_time_window": str,
                "pickup_confirmation_started_at": str,
                "user_confirmed_pickup": bool,
                "owner_confirmed_pickup": bool,
                "return_confirmation_started_at": str,
                "user_confirmed_return": bool,
                "owner_confirmed_return": bool,
                "cost": int,
                "meetup_date": str,
                "meetup_time": str,
                "rent_start_date": str,
                "rent_end_date": str
            }
        ]

    Possible errors:
        401 if the user is not authenticated
        500 if an unexpected error occurs
    """
    return RentalsController.get_user_rentals_controller()


@rentals_bp.route("/my-lendings", methods=["GET"])
@jwt_required()
def get_my_lendings() -> tuple[Response, int]:
    """
    Retrieve all active lendings for the authenticated user.

    This endpoint returns lendings with statuses:
    'pending', 'approved', 'awaiting_pickup_confirmation', 'ongoing', 'awaiting_return_confirmation'

    Response JSON:
        [
            {
                "rental_id": str,
                "rent_status": str,
                "book_id": str,
                "title": str,
                "author": str,
                "image": str,
                "from": str,
                "all_fees_captured": bool,
                "reserved_at": str,
                "reservation_expires_at": str,
                "rental_duration_days": int,
                "meetup_location": str,
                "meetup_time_window": str,
                "pickup_confirmation_started_at": str,
                "user_confirmed_pickup": bool,
                "owner_confirmed_pickup": bool,
                "return_confirmation_started_at": str,
                "user_confirmed_return": bool,
                "owner_confirmed_return": bool,
                "cost": int,
                "meetup_date": str,
                "meetup_time": str,
                "rent_start_date": str,
                "rent_end_date": str
            }
        ]
    """
    return RentalsController.get_user_lendings_controller()


@rentals_bp.route("/<rental_id>/approve", methods=["POST"])
@jwt_required()
def approve_rental(rental_id: str) -> tuple[Response, int]:
    """
    Approve a rental request and set meetup time.
    """
    return RentalsController.approve_rental_controller(rental_id)


@rentals_bp.route("/<rental_id>/reject", methods=["POST"])
@jwt_required()
def reject_rental(rental_id: str) -> tuple[Response, int]:
    """
    Reject a rental request and release reserved funds.

    Request Body:
        {
            "reason": str (optional)
        }

    Response:
        {
            "message": str,
            "result": {
                "rental_id": str,
                "reason": str,
                "released_amount": int
            }
        }
    """
    return RentalsController.reject_rental_controller(rental_id)


@rentals_bp.route("/<rental_id>/cancel", methods=["POST"])
@jwt_required()
def cancel_rental(rental_id: str) -> tuple[Response, int]:
    """
    Cancel a rental request by the renter and release reserved funds.

    Response:
        {
            "message": str,
            "result": {
                "rental_id": str,
                "released_amount": int
            }
        }
    """
    return RentalsController.cancel_rental_controller(rental_id)


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


@rentals_bp.route("/test", methods=["GET"])
@jwt_required()
def test_route():
    return jsonify({"message": "Rentals routes working!"}), 200


@rentals_bp.route("/cleanup", methods=["POST"])
def cleanup_expired_rentals_manual() -> tuple[Response, int]:
    """
    Manual endpoint to trigger cleanup of expired rentals.
    """
    try:
        from app.scheduler import run_cleanup_now
        from flask import current_app

        result = run_cleanup_now(current_app._get_current_object())

        return (
            jsonify(
                {
                    "message": "Cleanup completed",
                    "cleaned": result["cleaned"],
                    "errors": result["errors"],
                }
            ),
            200,
        )

    except Exception as e:
        print(f"Error in cleanup: {str(e)}")
        return jsonify({"error": str(e)}), 500


@rentals_bp.route("/status-update", methods=["POST"])
def update_rental_statuses_manual() -> tuple[Response, int]:
    """
    Manual endpoint to trigger rental status updates.
    """
    try:
        from app.scheduler import run_status_update_now
        from flask import current_app

        result = run_status_update_now(current_app._get_current_object())

        return (
            jsonify(
                {
                    "message": "Status update completed",
                    "pickup_updates": result["pickup_updates"]["updated"],
                    "return_updates": result["return_updates"]["updated"],
                }
            ),
            200,
        )

    except Exception as e:
        print(f"Error in status update: {str(e)}")
        return jsonify({"error": str(e)}), 500


@rentals_bp.route("/<rental_id>/confirm-pickup", methods=["POST"])
@jwt_required()
def confirm_pickup(rental_id: str) -> tuple[Response, int]:
    """
    Confirm book pickup by either renter or owner.
    """
    return RentalsController.confirm_pickup_controller(rental_id)


@rentals_bp.route("/<rental_id>/confirm-return", methods=["POST"])
@jwt_required()
def confirm_return(rental_id: str) -> tuple[Response, int]:
    """
    Confirm book return by either renter or owner.
    """
    return RentalsController.confirm_return_controller(rental_id)
