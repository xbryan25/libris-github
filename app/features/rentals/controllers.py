from flask import request, jsonify, make_response, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
import traceback
import datetime

from .services import RentalsServices

from .repository import RentalsRepository

from ..notifications.services import NotificationServices

from ..books.services import BookServices

from ..users.services import UserServices

from app.common.constants import NotificationMessages

from app.exceptions.custom_exceptions import EntityNotFoundError


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
            - latitude: Latitude of the meetup location
            - longitude: Longitude of the meetup location
            - meetup_date: Date for meetup (ISO 8601)
            - actual_rate: Daily rental rate at time of booking
            - actual_deposit: Security deposit at time of booking

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
                "bookId",
                "totalRentCost",
                "meetupTimeWindow",
                "meetupLocation",
                "latitude",
                "longitude",
                "meetupDate",
                "actualRate",
                "actualDeposit",
                "ownerUserId",
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

            reserved_at = datetime.datetime.now()
            reservation_expires_at = reserved_at + datetime.timedelta(days=1)

            rental_data = {
                "user_id": current_user_id,
                "book_id": rental_data_json["bookId"],
                "reserved_at": reserved_at,
                "reservation_expires_at": reservation_expires_at,
                "total_rent_cost": rental_data_json["totalRentCost"],
                "meetup_time_window": rental_data_json["meetupTimeWindow"],
                "meetup_location": rental_data_json["meetupLocation"],
                "latitude": float(rental_data_json["latitude"]),
                "longitude": float(rental_data_json["longitude"]),
                "meetup_date": rental_data_json["meetupDate"],
                "actual_rate": rental_data_json["actualRate"],
                "actual_deposit": rental_data_json["actualDeposit"],
                "original_owner_id": rental_data_json["ownerUserId"],
            }

            result = RentalsServices.create_rental_service(rental_data)

            if result is None:
                return (
                    jsonify(
                        {
                            "error": "Failed to create rental. You may have insufficient balance."
                        }
                    ),
                    400,
                )

            resp = make_response(
                {
                    "rental_id": result["rental_id"],
                    "messageTitle": "Rental request created successfully.",
                    "message": "Your rental request has been sent.",
                }
            )

            book_details = BookServices.get_book_details_service(rental_data["book_id"])

            owner_id = str(book_details["owner_user_id"]) if book_details else None

            renter_username = UserServices.get_username_service(current_user_id)

            notification_header = NotificationMessages.RENTAL_REQUEST_HEADER
            notification_message = NotificationMessages.RENTAL_REQUEST_MESSAGE.format(
                username=renter_username,
                title=f"{book_details['title'] if book_details else None}",
            )

            NotificationServices.add_notification_service(
                current_user_id,
                owner_id,
                "rent",
                notification_header,
                notification_message,
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
            exists = RentalsServices.check_pending_rental(current_user_id, book_id)
            return jsonify({"exists": exists}), 200
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_rentals_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            rentals = RentalsServices.get_user_rentals_with_status(user_id)

            return jsonify(rentals), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_completed_rental_controller(rental_id: str) -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            completed_rental = RentalsServices.get_completed_rental_service(
                user_id, rental_id
            )

            return jsonify(completed_rental), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_completed_rentals_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            params = {
                "sort_by": (request.args.get("sortBy", "start date")).strip().lower(),
                "sort_order": (request.args.get("sortOrder", "newest first"))
                .strip()
                .lower(),
                "cards_per_page": int(request.args.get("cardsPerPage", 5)),
                "page_number": int(request.args.get("pageNumber", 1)),
            }

            completed_rentals = RentalsServices.get_user_completed_rentals_service(
                user_id, params
            )

            return jsonify(completed_rentals), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_completed_rentals_count_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            completed_rentals_count = (
                RentalsServices.get_user_completed_rentals_count_service(user_id)
            )
            return jsonify({"count": completed_rentals_count}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_lendings_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            lendings = RentalsServices.get_user_lendings_with_status(user_id)

            return jsonify(lendings), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_completed_lending_controller(rental_id: str) -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            completed_lending = RentalsServices.get_completed_lending_service(
                user_id, rental_id
            )

            return jsonify(completed_lending), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_completed_lendings_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            params = {
                "sort_by": (request.args.get("sortBy", "start date")).strip().lower(),
                "sort_order": (request.args.get("sortOrder", "newest first"))
                .strip()
                .lower(),
                "cards_per_page": int(request.args.get("cardsPerPage", 5)),
                "page_number": int(request.args.get("pageNumber", 1)),
            }

            completed_lendings = RentalsServices.get_user_completed_lendings_service(
                user_id, params
            )

            return jsonify(completed_lendings), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_completed_lendings_count_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            completed_lendings_count = (
                RentalsServices.get_user_completed_lendings_count_service(user_id)
            )

            return jsonify({"count": completed_lendings_count}), 200

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

            result, error, book_id, renter_id = RentalsServices.approve_rental_request(
                rental_id, meetup_time, user_id
            )

            if error:
                return jsonify({"error": error}), 400

            if not book_id:
                raise EntityNotFoundError(f"Book {book_id} does not exist.")

            book_details = BookServices.get_book_details_service(book_id)

            owner_username = UserServices.get_username_service(user_id)

            notification_header = NotificationMessages.RENTAL_REQUEST_APPROVED_HEADER
            notification_message = (
                NotificationMessages.RENTAL_REQUEST_APPROVED_MESSAGE.format(
                    title=f"{book_details['title'] if book_details else None}",
                    username=owner_username,
                )
            )

            NotificationServices.add_notification_service(
                user_id,
                renter_id,
                "rent",
                notification_header,
                notification_message,
            )

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

            result, error, renter_id = RentalsServices.reject_rental_request(
                rental_id, reason, user_id
            )

            if error:
                return jsonify({"error": error}), 400

            book_id = RentalsRepository.get_book_id_from_rental(rental_id)

            if not book_id:
                raise EntityNotFoundError(f"Book {book_id} does not exist.")

            book_details = BookServices.get_book_details_service(book_id)

            owner_username = UserServices.get_username_service(user_id)

            notification_header = NotificationMessages.RENTAL_REQUEST_REJECTED_HEADER
            notification_message = (
                NotificationMessages.RENTAL_REQUEST_REJECTED_MESSAGE.format(
                    title=f"{book_details['title'] if book_details else None}",
                    username=owner_username,
                    reason=reason,
                )
            )

            # Delete the rental entry before sending the notification
            RentalsRepository.delete_rental(rental_id)

            NotificationServices.add_notification_service(
                user_id,
                renter_id,
                "rent",
                notification_header,
                notification_message,
            )

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

    @staticmethod
    def cancel_rental_controller(rental_id: str) -> tuple[Response, int]:
        """
        Controller to cancel a rental request by the renter.
        This will delete the rental entry and release reserved funds.
        """
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            result, error = RentalsServices.cancel_rental_request(rental_id, user_id)

            if error:
                return jsonify({"error": error}), 400

            book_id = RentalsRepository.get_book_id_from_rental(rental_id)

            if not book_id:
                raise EntityNotFoundError(f"Book {book_id} does not exist.")

            book_details = BookServices.get_book_details_service(book_id)

            owner_id = str(book_details["owner_user_id"]) if book_details else None

            renter_username = UserServices.get_username_service(user_id)

            notification_header = NotificationMessages.RENTAL_REQUEST_CANCELLED_HEADER
            notification_message = (
                NotificationMessages.RENTAL_REQUEST_CANCELLED_MESSAGE.format(
                    title=f"{book_details['title'] if book_details else None}",
                    username=renter_username,
                )
            )

            # Delete the rental entry before sending the notification
            RentalsRepository.delete_rental(rental_id)

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
                        "message": "Rental cancelled successfully. Reserved funds have been released.",
                        "result": result,
                    }
                ),
                200,
            )
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def confirm_pickup_controller(rental_id: str) -> tuple[Response, int]:
        """
        Controller to confirm book pickup by either user or owner.
        """
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            result, error, owner_id, renter_id = RentalsServices.confirm_pickup(
                rental_id, user_id
            )

            if not result:
                raise EntityNotFoundError(
                    "There was an error in confirming book pickup."
                )

            if error:
                return jsonify({"error": error}), 400

            book_id = RentalsRepository.get_book_id_from_rental(rental_id)

            if not book_id:
                raise EntityNotFoundError(f"Book {book_id} does not exist.")

            book_details = BookServices.get_book_details_service(book_id)

            owner_username = UserServices.get_username_service(owner_id)
            renter_username = UserServices.get_username_service(renter_id)

            # If both result["owner_confirmed_pickup"] and result["user_confirmed_pickup"] are both True,
            # emit RENTAL_STARTED notification,
            # otherwise emit CONFIRM_BOOK_PICKUP notification

            if result["owner_confirmed_pickup"] and not result["user_confirmed_pickup"]:
                notification_header = (
                    NotificationMessages.RENTAL_CONFIRM_BOOK_PICKUP_HEADER
                )
                notification_message = NotificationMessages.RENTAL_CONFIRM_BOOK_PICKUP_RENTER_MESSAGE.format(
                    username=owner_username,
                    title=f"{book_details['title'] if book_details else None}",
                )

                NotificationServices.add_notification_service(
                    owner_id,
                    renter_id,
                    "rent",
                    notification_header,
                    notification_message,
                )
            elif (
                not result["owner_confirmed_pickup"] and result["user_confirmed_pickup"]
            ):
                notification_header = (
                    NotificationMessages.RENTAL_CONFIRM_BOOK_PICKUP_HEADER
                )
                notification_message = NotificationMessages.RENTAL_CONFIRM_BOOK_PICKUP_OWNER_MESSAGE.format(
                    username=renter_username,
                    title=f"{book_details['title'] if book_details else None}",
                )

                NotificationServices.add_notification_service(
                    renter_id,
                    owner_id,
                    "rent",
                    notification_header,
                    notification_message,
                )
            else:
                notification_header = NotificationMessages.RENTAL_STARTED_HEADER
                notification_message = (
                    NotificationMessages.RENTAL_STARTED_MESSAGE.format(
                        username=owner_username,
                        title=f"{book_details['title'] if book_details else None}",
                    )
                )

                NotificationServices.add_notification_service(
                    owner_id,
                    renter_id,
                    "rent",
                    notification_header,
                    notification_message,
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
    def confirm_return_controller(rental_id: str) -> tuple[Response, int]:
        """
        Controller to confirm book return by either user or owner.
        """
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            result, error, owner_id, renter_id = RentalsServices.confirm_return(
                rental_id, user_id
            )

            if not result:
                raise EntityNotFoundError(
                    "There was an error in confirming book return."
                )

            if error:
                return jsonify({"error": error}), 400

            book_id = RentalsRepository.get_book_id_from_rental(rental_id)

            if not book_id:
                raise EntityNotFoundError(f"Book {book_id} does not exist.")

            book_details = BookServices.get_book_details_service(book_id)

            owner_username = UserServices.get_username_service(owner_id)
            renter_username = UserServices.get_username_service(renter_id)

            # If both result["owner_confirmed_return"] and result["user_confirmed_return"] are both True,
            # emit RENTAL_COMPLETED notification,
            # otherwise emit CONFIRM_BOOK_RETURN notification

            if result["owner_confirmed_return"] and not result["user_confirmed_return"]:
                notification_header = (
                    NotificationMessages.RENTAL_RETURN_VERIFICATION_NEEDED_HEADER
                )
                notification_message = NotificationMessages.RENTAL_RETURN_VERIFICATION_NEEDED_RENTER_MESSAGE.format(
                    username=owner_username,
                    title=f"{book_details['title'] if book_details else None}",
                )

                NotificationServices.add_notification_service(
                    owner_id,
                    renter_id,
                    "rent",
                    notification_header,
                    notification_message,
                )
            elif (
                not result["owner_confirmed_return"] and result["user_confirmed_return"]
            ):
                notification_header = (
                    NotificationMessages.RENTAL_RETURN_VERIFICATION_NEEDED_HEADER
                )
                notification_message = NotificationMessages.RENTAL_RETURN_VERIFICATION_NEEDED_OWNER_MESSAGE.format(
                    username=renter_username,
                    title=f"{book_details['title'] if book_details else None}",
                )

                NotificationServices.add_notification_service(
                    renter_id,
                    owner_id,
                    "rent",
                    notification_header,
                    notification_message,
                )
            else:
                notification_header = NotificationMessages.RENTAL_COMPLETED_HEADER
                notification_message_renter = (
                    NotificationMessages.RETURN_COMPLETED_RENTER_MESSAGE.format(
                        title=f"{book_details['title'] if book_details else None}",
                        username=owner_username,
                    )
                )

                notification_message_owner = (
                    NotificationMessages.RETURN_COMPLETED_OWNER_MESSAGE.format(
                        title=f"{book_details['title'] if book_details else None}",
                        username=renter_username,
                    )
                )

                NotificationServices.add_notification_service(
                    owner_id,
                    renter_id,
                    "rent",
                    notification_header,
                    notification_message_renter,
                )

                NotificationServices.add_notification_service(
                    renter_id,
                    owner_id,
                    "rent",
                    notification_header,
                    notification_message_owner,
                )

            return (
                jsonify(
                    {
                        "message": "Return confirmed successfully.",
                        "result": result,
                    }
                ),
                200,
            )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
