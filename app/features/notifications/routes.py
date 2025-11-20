from flask import Blueprint, Response
from .controllers import NotificationControllers

from flask_jwt_extended import jwt_required

notifications_bp = Blueprint("notifications_bp", __name__)


@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def get_notifications() -> tuple[Response, int]:
    """
    (add later)
    """

    return NotificationControllers.get_notifications_controller()
