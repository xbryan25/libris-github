from flask import request, jsonify, Response

import traceback

from flask_jwt_extended import get_jwt_identity

from .services import NotificationServices

from app.exceptions.custom_exceptions import InvalidParameterError

from app.utils import dict_keys_to_camel, asdict_enum_safe, to_int

from typing import Any, cast


class NotificationControllers:

    @staticmethod
    def get_notifications_controller() -> tuple[Response, int]:
        """add later"""

        ALLOWED_READ_STATUS_ITEMS = {"show all", "show only read", "show only unread"}
        ALLOWED_ORDER_ITEMS = {"show newest first", "show oldest first"}

        try:

            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated."}), 401

            params = {
                "rows_per_page": to_int(request.args.get("rowsPerPage", 0)),
                "page_number": to_int(request.args.get("pageNumber", 0)),
                "read_status": (request.args.get("readStatus") or "").strip().lower(),
                "order": (request.args.get("order") or "").strip().lower(),
            }

            if int(params["rows_per_page"]) < 0:
                raise InvalidParameterError(
                    f"Invalid 'rows_per_page' value: '{params['rows_per_page']}'. Must be a positive integer."
                )

            if int(params["page_number"]) < 0:
                raise InvalidParameterError(
                    f"Invalid 'pageNumber' value: '{params['page_number']}'. Must be a positive integer."
                )

            if params["read_status"] not in ALLOWED_READ_STATUS_ITEMS:
                raise InvalidParameterError(
                    f"""Invalid 'readStatus' value: '{params['read_status']}'.
                    Must be one of: ['show all', 'show only read', 'show only unread']."""
                )

            if params["order"] not in ALLOWED_ORDER_ITEMS:
                raise InvalidParameterError(
                    f"""Invalid 'order' value: '{params['order']}'.
                    Must be one of: ['show newest first', 'show oldest first']."""
                )

            notifications = NotificationServices.get_notifications_service(
                user_id, params
            )

            return (
                jsonify(
                    [
                        dict_keys_to_camel(
                            cast(dict[str, Any], asdict_enum_safe(notification))
                        )
                        for notification in notifications
                    ]
                ),
                200,
            )

        except InvalidParameterError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except (ValueError, TypeError):
            traceback.print_exc()
            return (
                jsonify(
                    {
                        "error": "Invalid query parameter. 'rowsPerPage' and 'pageNumber' must be positive integers."
                    }
                ),
                400,
            )

    @staticmethod
    def get_notifications_total_count_controller() -> tuple[Response, int]:
        """add later"""

        ALLOWED_READ_STATUS_ITEMS = {"show all", "show only read", "show only unread"}

        try:

            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated."}), 401

            params = {
                "read_status": (request.args.get("readStatus") or "").strip().lower(),
            }

            if params["read_status"] not in ALLOWED_READ_STATUS_ITEMS:
                raise InvalidParameterError(
                    f"""Invalid 'readStatus' value: '{params['read_status']}'.
                    Must be one of: ['show all', 'show only read', 'show only unread']."""
                )

            notifications_count = (
                NotificationServices.get_notifications_total_count_service(
                    user_id, params
                )
            )

            return (
                jsonify({"totalCount": notifications_count}),
                200,
            )

        except InvalidParameterError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400
