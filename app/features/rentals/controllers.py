from flask import jsonify, Response, request
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

            return jsonify(rentals), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_lendings_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            lendings = RentalServices.get_user_lendings_with_status(user_id)

            return jsonify(lendings), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def approve_rental_controller(rental_id: str) -> tuple[Response, int]:
        """
        Controller to approve a rental request.
        This will capture fees, deduct from wallet, and log transaction.
        """
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            # Get request data
            data = request.get_json()

            if not data:
                return jsonify({"error": "Invalid request body"}), 400

            meetup_time = data.get("meetupTime")

            if not meetup_time:
                return jsonify({"error": "Meetup time is required"}), 400

            result, error = RentalServices.approve_rental_request(
                rental_id, meetup_time, user_id
            )

            if error:
                return jsonify({"error": error}), 400

            return (
                jsonify(
                    {
                        "message": "Rental approved successfully. Fees captured and transaction logged.",
                        "rental": result,
                    }
                ),
                200,
            )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def reject_rental_controller(rental_id: str) -> tuple[Response, int]:
        """
        Controller to reject a rental request.
        This will delete the rental entry and release reserved funds.
        """
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            # Get request data
            data = request.get_json()

            if not data:
                return jsonify({"error": "Invalid request body"}), 400

            reason = data.get("reason", "No reason provided")

            result, error = RentalServices.reject_rental_request(
                rental_id, reason, user_id
            )

            if error:
                return jsonify({"error": error}), 400

            return (
                jsonify(
                    {
                        "message": "Rental rejected successfully. Reserved funds have been released.",
                        "result": result,
                    }
                ),
                200,
            )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
