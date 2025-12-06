from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

from .controllers import RatingControllers

ratings_bp = Blueprint("ratings_bp", __name__)


@ratings_bp.route("/rental/<rental_id>/rate", methods=["POST"])
@jwt_required()
def submit_rental_rating(rental_id: str) -> tuple[Response, int]:
    """Submit a rating for a rental."""
    return RatingControllers.submit_rental_rating(rental_id)


@ratings_bp.route("/purchase/<purchase_id>/rate", methods=["POST"])
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
