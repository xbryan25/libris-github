from flask import request, jsonify, make_response, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
import traceback
import datetime

from .services import PurchasesServices


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

            reserved_at = datetime.datetime.now()
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

            result = PurchasesServices.create_purchase_service(purchase_data)

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
            exists = PurchasesServices.check_pending_purchase(current_user_id, book_id)
            return jsonify({"exists": exists}), 200
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_purchases_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            purchases = PurchasesServices.get_user_purchases_with_status(user_id)

            return jsonify(purchases), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_sales_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            sales = PurchasesServices.get_user_sales_with_status(user_id)

            return jsonify(sales), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def approve_purchase_controller(purchase_id: str) -> tuple[Response, int]:
        """
        Controller to approve a purchase request.
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

            result, error = PurchasesServices.approve_purchase_request(
                purchase_id, meetup_time, user_id
            )

            if error:
                return jsonify({"error": error}), 400

            return (
                jsonify(
                    {
                        "message": "Purchase approved successfully. Fees captured and transaction logged.",
                        "purchase": result,
                    }
                ),
                200,
            )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def reject_purchase_controller(purchase_id: str) -> tuple[Response, int]:
        """
        Controller to reject a purchase request.
        This will delete the purchase entry and release reserved funds.
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

            result, error = PurchasesServices.reject_purchase_request(
                purchase_id, reason, user_id
            )

            if error:
                return jsonify({"error": error}), 400

            return (
                jsonify(
                    {
                        "message": "Purchase rejected successfully. Reserved funds have been released.",
                        "result": result,
                    }
                ),
                200,
            )
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def cancel_purchase_controller(purchase_id: str) -> tuple[Response, int]:
        """
        Controller to cancel a purchase request by the buyer.
        This will delete the purchase entry and release reserved funds.
        """
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            result, error = PurchasesServices.cancel_purchase_request(
                purchase_id, user_id
            )

            if error:
                return jsonify({"error": error}), 400

            return (
                jsonify(
                    {
                        "message": "Purchase cancelled successfully. Reserved funds have been released.",
                        "result": result,
                    }
                ),
                200,
            )
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def confirm_pickup_controller(purchase_id: str) -> tuple[Response, int]:
        """
        Controller to confirm book pickup by either buyer or owner.
        """
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            result, error = PurchasesServices.confirm_pickup(purchase_id, user_id)

            if error:
                return jsonify({"error": error}), 400

            return (
                jsonify(
                    {
                        "message": "Pickup confirmed successfully.",
                        "result": result,
                    }
                ),
                200,
            )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def process_transfer_decision_controller(purchase_id: str) -> tuple[Response, int]:
        """
        Controller to process the buyer's final ownership transfer decision.
        """
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            decision_data = request.get_json()
            if decision_data is None or "transfer_ownership" not in decision_data:
                return (
                    jsonify({"error": "Missing 'transfer_ownership' in request body."}),
                    400,
                )

            transfer_ownership = decision_data["transfer_ownership"]

            if not isinstance(transfer_ownership, bool):
                return (
                    jsonify({"error": "'transfer_ownership' must be a boolean."}),
                    400,
                )

            result, error = PurchasesServices.process_transfer_decision_service(
                purchase_id, transfer_ownership, user_id
            )

            if error:
                return jsonify({"error": error}), 400

            return (
                jsonify(
                    {
                        "message": "Ownership transfer decision recorded successfully.",
                        "result": result,
                    }
                ),
                200,
            )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
