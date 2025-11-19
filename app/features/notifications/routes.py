from flask import Blueprint, Response
from .controllers import NotificationControllers

from flask_jwt_extended import jwt_required

notifications_bp = Blueprint("notifications_bp", __name__)


@notifications_bp.route("/get-recent-notifications", methods=["GET"])
@jwt_required()
def get_recent_notifications() -> tuple[Response, int]:
    """
    (add later)
    """
    return NotificationControllers.get_recent_notifications_controller()
