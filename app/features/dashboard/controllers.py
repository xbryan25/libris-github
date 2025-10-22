from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from .services import DashboardServices
import traceback


class DashboardController:

    @staticmethod
    def get_summary_controller() -> tuple[dict, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            summary = DashboardServices.get_user_dashboard(user_id)
            return jsonify(summary), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
