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


@notifications_bp.route("/total-count", methods=["GET"])
@jwt_required()
def get_notifications_total_count() -> tuple[Response, int]:
    """
    (add later)
    """

    return NotificationControllers.get_notifications_total_count_controller()


@notifications_bp.route("/<string:notification_id>/mark-as-read", methods=["PATCH"])
@jwt_required()
def mark_notification_as_read(notification_id: str) -> tuple[Response, int]:
    """
    (add later)
    """

    return NotificationControllers.mark_notification_as_read_controller(notification_id)


@notifications_bp.route("/mark-as-read", methods=["PATCH"])
@jwt_required()
def mark_multiple_notifications_as_read() -> tuple[Response, int]:
    """
    (add later)
    """

    return NotificationControllers.mark_multiple_notifications_as_read_controller()
