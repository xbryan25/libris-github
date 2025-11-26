from flask import Blueprint, Response
from .controllers import RentalControllers
from flask_jwt_extended import jwt_required

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
    return RentalControllers.get_user_rentals_controller()


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
    return RentalControllers.get_user_lendings_controller()


@rentals_bp.route("/<rental_id>/approve", methods=["POST"])
@jwt_required()
def approve_rental(rental_id: str) -> tuple[Response, int]:
    """
    Approve a rental request and set meetup time.
    """
    return RentalControllers.approve_rental_controller(rental_id)


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
    return RentalControllers.reject_rental_controller(rental_id)
