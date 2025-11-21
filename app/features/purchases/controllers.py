from flask import request, jsonify, make_response, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
import traceback
import datetime

from .services import PurchasesService


class PurchasesController:

    @staticmethod
    @jwt_required()
    def create_purchase_controller() -> tuple[Response, int]:
        """
        Handle creation of a new purchase.

        Expects JSON body:
            - book_id: UUID of the book
            - total_buy_cost: Total cost of purchase
            - meetup_time_window: Preferred time window for meetup
            - meetup_location: Meetup location
            - meetup_date: Date of meetup (ISO 8601)

        Backend defaults:
            - purchase_status: "pending"
            - reserved_at: current UTC timestamp
            - reservation_expires_at: reserved_at + 1 day
            - all_fees_captured: False

        Response JSON:
            - purchase_id: UUID of created purchase
            - messageTitle: Success message
            - message: Detailed message

        Errors:
            400 if required fields are missing
            401 if user is not authenticated
            500 if unexpected error occurs
        """
        try:
            current_user_id = get_jwt_identity()
            purchase_data_json = request.get_json()

            if not purchase_data_json:
                return jsonify({"error": "Request body is required."}), 400

            required_fields = [
                "book_id",
                "total_buy_cost",
                "meetup_time_window",
                "meetup_location",
                "meetup_date",
            ]

            missing_fields = [
                field for field in required_fields if not purchase_data_json.get(field)
            ]
            if missing_fields:
                return (
                    jsonify(
                        {
                            "error": f"Missing required fields: {', '.join(missing_fields)}"
                        }
                    ),
                    400,
                )

            reserved_at = datetime.datetime.now(datetime.timezone.utc)
            reservation_expires_at = reserved_at + datetime.timedelta(days=1)

            purchase_data = {
                "user_id": current_user_id,
                "book_id": purchase_data_json["book_id"],
                "reserved_at": reserved_at,
                "reservation_expires_at": reservation_expires_at,
                "total_buy_cost": purchase_data_json["total_buy_cost"],
                "meetup_time_window": purchase_data_json["meetup_time_window"],
                "meetup_location": purchase_data_json["meetup_location"],
                "meetup_date": purchase_data_json["meetup_date"],
            }

            result = PurchasesService.create_purchase_service(purchase_data)

            if result is None:
                return jsonify({"error": "Failed to create purchase."}), 500

            resp = make_response(
                {
                    "purchase_id": result["purchase_id"],
                    "messageTitle": "Purchase created successfully.",
                    "message": "Your purchase request has been sent.",
                }
            )

            return resp, 201

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    @jwt_required()
    def check_purchase_controller(book_id: str) -> tuple[Response, int]:
        """
        Check if the current user already has a pending purchase for a given book.

        Args:
            book_id (str): The UUID of the book.

        Returns JSON:
            exists: True if a pending purchase exists, False otherwise.

        Errors:
            401 if user is not authenticated
            500 if unexpected error occurs
        """
        try:
            current_user_id = get_jwt_identity()
            exists = PurchasesService.check_pending_purchase(current_user_id, book_id)
            return jsonify({"exists": exists}), 200
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
