from flask import Blueprint, Response, jsonify
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


@purchases_bp.route("/my-purchases", methods=["GET"])
@jwt_required()
def get_my_purchases() -> tuple[Response, int]:
    """
    Retrieve all active purchases for the authenticated user.

    This endpoint returns purchases with statuses:
    'pending', 'approved', 'awaiting_pickup_confirmation', or completed but not rated

    Response JSON:
        [
            {
                "purchase_id": str,
                "purchase_status": str,
                "original_owner_id": str,
                "user_id": str,
                "book_id": str,
                "title": str,
                "author": str,
                "image": str,
                "from": str,
                "all_fees_captured": bool,
                "reserved_at": str,
                "reservation_expires_at": str,
                "meetup_location": str,
                "meetup_time_window": str,
                "meetup_time": str,
                "meetup_date": str,
                "pickup_confirmation_started_at": str,
                "user_confirmed_pickup": bool,
                "owner_confirmed_pickup": bool,
                "user_rated": bool,
                "owner_rated": bool,
                "cost": int
            }
        ]

    Possible errors:
        401 if the user is not authenticated
        500 if an unexpected error occurs
    """
    return PurchasesController.get_user_purchases_controller()


@purchases_bp.route("/completed/<string:purchase_id>", methods=["GET"])
@jwt_required()
def get_completed_purchase(purchase_id: str) -> tuple[Response, int]:
    """
    Retrieve a completed purchase for the authenticated user.

    Response JSON:
        {
            "purchase_id": str,
            "purchase_status": str,
            "original_owner_id": str,
            "user_id": str,
            "book_id": str,
            "title": str,
            "author": str,
            "image": str,
            "from": str,
            "all_fees_captured": bool,
            "reserved_at": str,
            "reservation_expires_at": str,
            "meetup_location": str,
            "meetup_time_window": str,
            "meetup_time": str,
            "meetup_date": str,
            "pickup_confirmation_started_at": str,
            "user_confirmed_pickup": bool,
            "owner_confirmed_pickup": bool,
            "user_rated": bool,
            "owner_rated": bool,
            "cost": int
        }


    Possible errors:
        401 if the user is not authenticated
        500 if an unexpected error occurs
    """
    return PurchasesController.get_completed_purchase_controller(purchase_id)


@purchases_bp.route("/my-completed-purchases", methods=["GET"])
@jwt_required()
def get_my_completed_purchases() -> tuple[Response, int]:
    """
    Retrieve all completed purchases for the authenticated user.

    Response JSON:
        [
            {
                "purchase_id": str,
                "purchase_status": str,
                "original_owner_id": str,
                "user_id": str,
                "book_id": str,
                "title": str,
                "author": str,
                "image": str,
                "from": str,
                "all_fees_captured": bool,
                "reserved_at": str,
                "reservation_expires_at": str,
                "meetup_location": str,
                "meetup_time_window": str,
                "meetup_time": str,
                "meetup_date": str,
                "pickup_confirmation_started_at": str,
                "user_confirmed_pickup": bool,
                "owner_confirmed_pickup": bool,
                "user_rated": bool,
                "owner_rated": bool,
                "cost": int
            }
        ]

    Possible errors:
        401 if the user is not authenticated
        500 if an unexpected error occurs
    """
    return PurchasesController.get_user_completed_purchases_controller()


@purchases_bp.route("/my-completed-purchases-count", methods=["GET"])
@jwt_required()
def get_my_completed_purchases_count() -> tuple[Response, int]:
    """
    Retrieve the total count of completed purchases for the authenticated user.

    Response JSON:
        { count: int }
    """
    return PurchasesController.get_user_completed_purchases_count_controller()


@purchases_bp.route("/my-sales", methods=["GET"])
@jwt_required()
def get_my_sales() -> tuple[Response, int]:
    """
    Retrieve all active sales for the authenticated user.

    This endpoint returns sales with statuses:
    'pending', 'approved', 'awaiting_pickup_confirmation', or completed but not rated

    Response JSON:
        [
            {
                "purchase_id": str,
                "purchase_status": str,
                "book_id": str,
                "title": str,
                "author": str,
                "image": str,
                "to": str,
                "all_fees_captured": bool,
                "reserved_at": str,
                "reservation_expires_at": str,
                "meetup_location": str,
                "meetup_time_window": str,
                "meetup_time": str,
                "meetup_date": str,
                "pickup_confirmation_started_at": str,
                "user_confirmed_pickup": bool,
                "owner_confirmed_pickup": bool,
                "user_rated": bool,
                "owner_rated": bool,
                "cost": int
            }
        ]
    """
    return PurchasesController.get_user_sales_controller()


@purchases_bp.route("/my-completed-sales", methods=["GET"])
@jwt_required()
def get_my_completed_sales() -> tuple[Response, int]:
    """
    Retrieve all completed sales for the authenticated user.

    Response JSON:
        [
            {
                "purchase_id": str,
                "purchase_status": str,
                "original_owner_id": str,
                "user_id": str,
                "book_id": str,
                "title": str,
                "author": str,
                "image": str,
                "from": str,
                "all_fees_captured": bool,
                "reserved_at": str,
                "reservation_expires_at": str,
                "meetup_location": str,
                "meetup_time_window": str,
                "meetup_time": str,
                "meetup_date": str,
                "pickup_confirmation_started_at": str,
                "user_confirmed_pickup": bool,
                "owner_confirmed_pickup": bool,
                "user_rated": bool,
                "owner_rated": bool,
                "cost": int
            }
        ]

    Possible errors:
        401 if the user is not authenticated
        500 if an unexpected error occurs
    """
    return PurchasesController.get_user_completed_sales_controller()


@purchases_bp.route("/my-completed-sales-count", methods=["GET"])
@jwt_required()
def get_my_completed_sales_count() -> tuple[Response, int]:
    """
    Retrieve the total count of completed sales for the authenticated user.

    Response JSON:
        { count: int }
    """
    return PurchasesController.get_user_completed_sales_count_controller()


@purchases_bp.route("/<purchase_id>/approve", methods=["POST"])
@jwt_required()
def approve_purchase(purchase_id: str) -> tuple[Response, int]:
    """
    Approve a purchase request and set meetup time.
    """
    return PurchasesController.approve_purchase_controller(purchase_id)


@purchases_bp.route("/<purchase_id>/reject", methods=["POST"])
@jwt_required()
def reject_purchase(purchase_id: str) -> tuple[Response, int]:
    """
    Reject a purchase request and release reserved funds.

    Request Body:
        {
            "reason": str (optional)
        }

    Response:
        {
            "message": str,
            "result": {
                "purchase_id": str,
                "reason": str,
                "released_amount": int
            }
        }
    """
    return PurchasesController.reject_purchase_controller(purchase_id)


@purchases_bp.route("/<purchase_id>/cancel", methods=["POST"])
@jwt_required()
def cancel_purchase(purchase_id: str) -> tuple[Response, int]:
    """
    Cancel a purchase request by the buyer and release reserved funds.

    Response:
        {
            "message": str,
            "result": {
                "purchase_id": str,
                "released_amount": int
            }
        }
    """
    return PurchasesController.cancel_purchase_controller(purchase_id)


@purchases_bp.route("/<purchase_id>/confirm-pickup", methods=["POST"])
@jwt_required()
def confirm_pickup(purchase_id: str) -> tuple[Response, int]:
    """
    Confirm book pickup by either buyer or owner.
    """
    return PurchasesController.confirm_pickup_controller(purchase_id)


@purchases_bp.route("/test", methods=["GET"])
@jwt_required()
def test_route():
    return jsonify({"message": "Purchases routes working!"}), 200


@purchases_bp.route("/<purchase_id>/transfer-decision", methods=["POST"])
@jwt_required()
def process_transfer_decision(purchase_id: str) -> tuple[Response, int]:
    """
    Process the buyer's final decision on book ownership transfer.

    Request Body:
        {
            "transfer_ownership": boolean
        }
    """
    return PurchasesController.process_transfer_decision_controller(purchase_id)
