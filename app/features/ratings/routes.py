from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

from .controllers import RatingControllers

ratings_bp = Blueprint("ratings_bp", __name__)


@ratings_bp.route("/rental/<rental_id>", methods=["POST"])
@jwt_required()
def submit_rental_rating(rental_id: str) -> tuple[Response, int]:
    """Submit a rating for a rental."""
    return RatingControllers.submit_rental_rating(rental_id)


@ratings_bp.route("/purchase/<purchase_id>", methods=["POST"])
@jwt_required()
def submit_purchase_rating(purchase_id: str) -> tuple[Response, int]:
    """
    Submit a rating for a purchase.

    Request body:
    {
        "rating": 5,
        "review": "Great transaction!",
        "from": "purchase" or "sale"
    }
    """
    return RatingControllers.submit_purchase_rating(purchase_id)


@ratings_bp.route("/purchase/<purchase_id>", methods=["GET"])
@jwt_required()
def get_ratings_from_purchase_for_user(purchase_id: str) -> tuple[Response, int]:
    """
    Get both received and given ratings from a purchase.

    Response body:
    {
        "given_rating": int,
        "given_comment": str,
        "received_rating": int,
        "received_comment": str,
    }
    """
    return RatingControllers.get_ratings_from_purchase_for_user_controller(purchase_id)
