from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

from .controllers import RatingControllers

ratings_bp = Blueprint("ratings_bp", __name__)


@ratings_bp.route("/<rental_id>/rate", methods=["POST"])
@jwt_required()
def submit_rating(rental_id: str) -> tuple[Response, int]:
    """Submit a rating for a rental."""
    return RatingControllers.submit_rating(rental_id)
