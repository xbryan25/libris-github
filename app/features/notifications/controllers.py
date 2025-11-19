from flask import request, jsonify, Response

import traceback

from flask_jwt_extended import get_jwt_identity

from .services import NotificationServices

from app.utils import dict_keys_to_camel, asdict_enum_safe

from typing import Any, cast


class NotificationControllers:

    @staticmethod
    def get_recent_notifications_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            params = {
                "num_of_notifications": int(request.args.get("numOfNotifications", 4))
            }

            recent_notifications = (
                NotificationServices.get_recent_notifications_service(
                    user_id, params["num_of_notifications"]
                )
            )

            return (
                jsonify(
                    [
                        dict_keys_to_camel(
                            cast(dict[str, Any], asdict_enum_safe(notification))
                        )
                        for notification in recent_notifications
                    ]
                ),
                200,
            )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
