from flask import request, jsonify, make_response, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
import traceback
import datetime

from .services import PurchasesServices

from .repository import PurchasesRepository

from ..notifications.services import NotificationServices

from ..books.services import BookServices

from ..users.services import UserServices

from app.common.constants import NotificationMessages

from app.exceptions.custom_exceptions import EntityNotFoundError


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

            book_details = BookServices.get_book_details_service(
                purchase_data_json["book_id"]
            )

            owner_id = str(book_details["owner_user_id"]) if book_details else None

            buyer_username = UserServices.get_username_service(current_user_id)

            notification_header = NotificationMessages.PURCHASE_REQUEST_HEADER
            notification_message = NotificationMessages.PURCHASE_REQUEST_MESSAGE.format(
                username=buyer_username,
                title=f"{book_details['title'] if book_details else None}",
            )

            NotificationServices.add_notification_service(
                current_user_id,
                owner_id,
                "purchase",
                notification_header,
                notification_message,
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
    def get_completed_purchase_controller(purchase_id: str) -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            completed_purchase = PurchasesServices.get_completed_purchase_service(
                user_id, purchase_id
            )

            return jsonify(completed_purchase), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_completed_purchases_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            params = {
                "sort_order": (request.args.get("sortOrder", "newest first"))
                .strip()
                .lower(),
                "cards_per_page": int(request.args.get("cardsPerPage", 5)),
                "page_number": int(request.args.get("pageNumber", 1)),
            }

            completed_purchases = (
                PurchasesServices.get_user_completed_purchases_service(user_id, params)
            )

            return jsonify(completed_purchases), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_completed_purchases_count_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            completed_purchases_count = (
                PurchasesServices.get_user_completed_purchases_count_service(user_id)
            )
            return jsonify({"count": completed_purchases_count}), 200

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
    def get_user_completed_sales_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            params = {
                "sort_order": (request.args.get("sortOrder", "newest first"))
                .strip()
                .lower(),
                "cards_per_page": int(request.args.get("cardsPerPage", 5)),
                "page_number": int(request.args.get("pageNumber", 1)),
            }

            completed_sales = PurchasesServices.get_user_completed_sales_service(
                user_id, params
            )

            return jsonify(completed_sales), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_completed_sales_count_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            completed_sales_count = (
                PurchasesServices.get_user_completed_sales_count_service(user_id)
            )
            return jsonify({"count": completed_sales_count}), 200

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

            result, error, book_id, buyer_id = (
                PurchasesServices.approve_purchase_request(
                    purchase_id, meetup_time, user_id
                )
            )

            if error:
                return jsonify({"error": error}), 400

            if not book_id:
                raise EntityNotFoundError(f"Book {book_id} does not exist.")

            book_details = BookServices.get_book_details_service(book_id)

            owner_username = UserServices.get_username_service(user_id)

            notification_header = NotificationMessages.PURCHASE_REQUEST_APPROVED_HEADER
            notification_message = (
                NotificationMessages.PURCHASE_REQUEST_APPROVED_MESSAGE.format(
                    title=f"{book_details['title'] if book_details else None}",
                    username=owner_username,
                )
            )

            NotificationServices.add_notification_service(
                user_id,
                buyer_id,
                "purchase",
                notification_header,
                notification_message,
            )

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

            result, error, buyer_id = PurchasesServices.reject_purchase_request(
                purchase_id, reason, user_id
            )

            if error:
                return jsonify({"error": error}), 400

            book_id = PurchasesRepository.get_book_id_from_purchase(purchase_id)

            if not book_id:
                raise EntityNotFoundError(f"Book {book_id} does not exist.")

            book_details = BookServices.get_book_details_service(book_id)

            owner_username = UserServices.get_username_service(user_id)

            notification_header = NotificationMessages.PURCHASE_REQUEST_REJECTED_HEADER
            notification_message = (
                NotificationMessages.PURCHASE_REQUEST_REJECTED_MESSAGE.format(
                    title=f"{book_details['title'] if book_details else None}",
                    username=owner_username,
                    reason=reason,
                )
            )

            # Delete the purchase entry before sending the notification
            PurchasesRepository.delete_purchase(purchase_id)

            NotificationServices.add_notification_service(
                user_id,
                buyer_id,
                "purchase",
                notification_header,
                notification_message,
            )

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

            book_id = PurchasesRepository.get_book_id_from_purchase(purchase_id)

            if not book_id:
                raise EntityNotFoundError(f"Book {book_id} does not exist.")

            book_details = BookServices.get_book_details_service(book_id)

            owner_id = str(book_details["owner_user_id"]) if book_details else None

            renter_username = UserServices.get_username_service(user_id)

            notification_header = NotificationMessages.PURCHASE_REQUEST_CANCELLED_HEADER
            notification_message = (
                NotificationMessages.PURCHASE_REQUEST_CANCELLED_MESSAGE.format(
                    title=f"{book_details['title'] if book_details else None}",
                    username=renter_username,
                )
            )

            # Delete the rental entry before sending the notification
            PurchasesRepository.delete_purchase(purchase_id)

            NotificationServices.add_notification_service(
                user_id,
                owner_id,
                "rent",
                notification_header,
                notification_message,
            )

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

            result, error, owner_id, buyer_id = PurchasesServices.confirm_pickup(
                purchase_id, user_id
            )

            if not result:
                raise EntityNotFoundError(
                    "There was an error in confirming book pickup."
                )

            if error:
                return jsonify({"error": error}), 400

            book_id = PurchasesRepository.get_book_id_from_purchase(purchase_id)

            if not book_id:
                raise EntityNotFoundError(f"Book {book_id} does not exist.")

            book_details = BookServices.get_book_details_service(book_id)

            owner_username = UserServices.get_username_service(owner_id)
            buyer_username = UserServices.get_username_service(buyer_id)

            # If both result["owner_confirmed_pickup"] and result["user_confirmed_pickup"] are both True,
            # emit PURCHASE_COMPLETED notification,
            # otherwise emit PURCHASE_CONFIRM_BOOK_PICKUP notification

            if result["owner_confirmed_pickup"] and not result["user_confirmed_pickup"]:
                notification_header = (
                    NotificationMessages.PURCHASE_CONFIRM_BOOK_PICKUP_HEADER
                )
                notification_message = NotificationMessages.PURCHASE_CONFIRM_BOOK_PICKUP_BUYER_MESSAGE.format(
                    username=owner_username,
                    title=f"{book_details['title'] if book_details else None}",
                )

                NotificationServices.add_notification_service(
                    owner_id,
                    buyer_id,
                    "rent",
                    notification_header,
                    notification_message,
                )
            elif (
                not result["owner_confirmed_pickup"] and result["user_confirmed_pickup"]
            ):
                notification_header = (
                    NotificationMessages.PURCHASE_CONFIRM_BOOK_PICKUP_HEADER
                )
                notification_message = NotificationMessages.PURCHASE_CONFIRM_BOOK_PICKUP_OWNER_MESSAGE.format(
                    username=buyer_username,
                    title=f"{book_details['title'] if book_details else None}",
                )

                NotificationServices.add_notification_service(
                    buyer_id,
                    owner_id,
                    "rent",
                    notification_header,
                    notification_message,
                )
            else:
                notification_header = NotificationMessages.PURCHASE_COMPLETED_HEADER
                notification_message_buyer = (
                    NotificationMessages.PURCHASE_COMPLETED_BUYER_MESSAGE.format(
                        title=f"{book_details['title'] if book_details else None}",
                        username=owner_username,
                    )
                )

                notification_message_owner = (
                    NotificationMessages.PURCHASE_COMPLETED_OWNER_MESSAGE.format(
                        title=f"{book_details['title'] if book_details else None}",
                        username=buyer_username,
                    )
                )

                NotificationServices.add_notification_service(
                    owner_id,
                    buyer_id,
                    "rent",
                    notification_header,
                    notification_message_buyer,
                )

                NotificationServices.add_notification_service(
                    buyer_id,
                    owner_id,
                    "rent",
                    notification_header,
                    notification_message_owner,
                )

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
