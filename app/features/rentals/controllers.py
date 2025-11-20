from flask import jsonify, Response
import traceback
from flask_jwt_extended import get_jwt_identity
from .services import RentalServices


class RentalControllers:
    @staticmethod
    def get_user_rentals_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            rentals = RentalServices.get_user_rentals_with_status(user_id)

            if not rentals:
                return jsonify({"error": "No rentals found for this user"}), 404

            return jsonify(rentals), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
