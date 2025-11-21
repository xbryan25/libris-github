from flask import request, jsonify, make_response, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
import traceback
import datetime


from .services import RentalsService


class RentalsController:

    @staticmethod
    @jwt_required()
    def create_rental_controller() -> tuple[Response, int]:
        """
        Handle creation of a new rental request.

        Expects JSON body:
            - book_id: UUID of the book
            - total_rent_cost: Total cost of rental
            - rental_duration_days: Number of days to rent
            - meetup_time_window: Preferred time window for meetup
            - meetup_location: Location for meetup
            - meetup_date: Date for meetup (ISO 8601)

        Backend defaults:
            - rent_status: "pending"
            - reserved_at: current UTC timestamp
            - reservation_expires_at: reserved_at + 1 day
            - all_fees_captured: False

        Response JSON:
            - rental_id: UUID of created rental
            - messageTitle: Success message
            - message: Detailed message

        Errors:
            400 if required fields are missing
            401 if user is not authenticated
            500 if unexpected error occurs
        """
        try:
            current_user_id = get_jwt_identity()
            rental_data_json = request.get_json()

            if not rental_data_json:
                return jsonify({"error": "Request body is required."}), 400

            required_fields = [
                "book_id",
                "total_rent_cost",
                "rental_duration_days",
                "meetup_time_window",
                "meetup_location",
                "meetup_date",
            ]

            missing_fields = [
                field for field in required_fields if not rental_data_json.get(field)
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

            reserved_at = datetime.datetime.now(datetime.UTC)
            reservation_expires_at = reserved_at + datetime.timedelta(days=1)

            rental_data = {
                "user_id": current_user_id,
                "book_id": rental_data_json["book_id"],
                "reserved_at": reserved_at,
                "reservation_expires_at": reservation_expires_at,
                "total_rent_cost": rental_data_json["total_rent_cost"],
                "rental_duration_days": rental_data_json["rental_duration_days"],
                "meetup_time_window": rental_data_json["meetup_time_window"],
                "meetup_location": rental_data_json["meetup_location"],
                "meetup_date": rental_data_json["meetup_date"],
            }

            result = RentalsService.create_rental_service(rental_data)

            if result is None:
                return jsonify({"error": "Failed to create rental."}), 500

            resp = make_response(
                {
                    "rental_id": result["rental_id"],
                    "messageTitle": "Rental request created successfully.",
                    "message": "Your rental request has been sent.",
                }
            )

            return resp, 201

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    @jwt_required()
    def check_rental_controller(book_id: str) -> tuple[Response, int]:
        """
        Check if the current user already has a pending rental request for a given book.

        Args:
            book_id (str): The UUID of the book.

        Returns JSON:
            exists: True if a pending rental exists, False otherwise.

        Errors:
            401 if user is not authenticated
            500 if unexpected error occurs
        """
        try:
            current_user_id = get_jwt_identity()
            exists = RentalsService.check_pending_rental(current_user_id, book_id)
            return jsonify({"exists": exists}), 200
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
