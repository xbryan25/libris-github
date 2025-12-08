from .repository import RentalsRepository
from app.features.wallets.repository import WalletRepository
from typing import Any
from app.utils import DateUtils
from datetime import datetime
import logging
import traceback

logger = logging.getLogger(__name__)


class RentalsServices:
    @staticmethod
    def get_user_rentals_with_status(user_id: str) -> list[dict[str, Any]]:
        raw_rentals = RentalsRepository.get_user_rentals_with_status(user_id)

        formatted_rentals = []
        for rental in raw_rentals:
            formatted_rental = {
                "rental_id": rental.get("rental_id"),
                "rent_status": rental.get("rent_status"),
                "original_owner_id": rental.get("original_owner_id"),
                "user_id": rental.get("user_id"),
                "book_id": rental.get("book_id"),
                "title": rental.get("title", ""),
                "author": rental.get("author", ""),
                "image": rental.get("image"),
                "from": rental.get("from", ""),
                "actual_deposit": rental.get("actual_deposit", 0),
                "actual_rate": rental.get("actual_rate", 0),
                "all_fees_captured": rental.get("all_fees_captured", False),
                "reserved_at": DateUtils.format_datetime_to_iso(
                    rental.get("reserved_at")
                ),
                "reservation_expires_at": DateUtils.format_datetime_to_iso(
                    rental.get("reservation_expires_at")
                ),
                "rental_duration_days": rental.get("rental_duration_days", 0),
                "meetup_location": rental.get("meetup_location", ""),
                "meetup_time_window": rental.get("meetup_time_window", ""),
                "meetup_time": rental.get("meetup_time"),
                "pickup_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    rental.get("pickup_confirmation_started_at")
                ),
                "user_confirmed_pickup": rental.get("user_confirmed_pickup", False),
                "owner_confirmed_pickup": rental.get("owner_confirmed_pickup", False),
                "return_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    rental.get("return_confirmation_started_at")
                ),
                "user_confirmed_return": rental.get("user_confirmed_return", False),
                "owner_confirmed_return": rental.get("owner_confirmed_return", False),
                "cost": (
                    int(rental.get("cost", 0))
                    if rental.get("cost") not in (None, "")
                    else 0
                ),
                "meetup_date": (
                    DateUtils.extract_date(rental.get("meetup_date"))
                    if rental.get("meetup_date")
                    else None
                ),
                "rent_start_date": (
                    DateUtils.extract_date(rental.get("rent_start_date"))
                    if rental.get("rent_start_date")
                    else None
                ),
                "rent_end_date": (
                    DateUtils.extract_date(rental.get("rent_end_date"))
                    if rental.get("rent_end_date")
                    else None
                ),
            }
            formatted_rentals.append(formatted_rental)

        return formatted_rentals

    @staticmethod
    def get_completed_rental_service(
        user_id: str, rental_id: str
    ) -> dict[str, Any] | None:

        completed_rental = RentalsRepository.get_completed_rental(user_id, rental_id)

        if completed_rental:
            formatted_rental = {
                "rental_id": completed_rental.get("rental_id"),
                "rent_status": completed_rental.get("rent_status"),
                "original_owner_id": completed_rental.get("original_owner_id"),
                "user_id": completed_rental.get("user_id"),
                "book_id": completed_rental.get("book_id"),
                "title": completed_rental.get("title", ""),
                "author": completed_rental.get("author", ""),
                "image": completed_rental.get("image"),
                "from": completed_rental.get("from", ""),
                "actual_deposit": completed_rental.get("actual_deposit", 0),
                "actual_rate": completed_rental.get("actual_rate", 0),
                "all_fees_captured": completed_rental.get("all_fees_captured", False),
                "reserved_at": DateUtils.format_datetime_to_iso(
                    completed_rental.get("reserved_at")
                ),
                "reservation_expires_at": DateUtils.format_datetime_to_iso(
                    completed_rental.get("reservation_expires_at")
                ),
                "rental_duration_days": completed_rental.get("rental_duration_days", 0),
                "meetup_location": completed_rental.get("meetup_location", ""),
                "meetup_time_window": completed_rental.get("meetup_time_window", ""),
                "meetup_time": completed_rental.get("meetup_time"),
                "pickup_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    completed_rental.get("pickup_confirmation_started_at")
                ),
                "user_confirmed_pickup": completed_rental.get(
                    "user_confirmed_pickup", False
                ),
                "owner_confirmed_pickup": completed_rental.get(
                    "owner_confirmed_pickup", False
                ),
                "return_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    completed_rental.get("return_confirmation_started_at")
                ),
                "user_confirmed_return": completed_rental.get(
                    "user_confirmed_return", False
                ),
                "owner_confirmed_return": completed_rental.get(
                    "owner_confirmed_return", False
                ),
                "cost": (
                    int(completed_rental.get("cost", 0))
                    if completed_rental.get("cost") not in (None, "")
                    else 0
                ),
                "meetup_date": (
                    DateUtils.extract_date(completed_rental.get("meetup_date"))
                    if completed_rental.get("meetup_date")
                    else None
                ),
                "rent_start_date": (
                    DateUtils.extract_date(completed_rental.get("rent_start_date"))
                    if completed_rental.get("rent_start_date")
                    else None
                ),
                "rent_end_date": (
                    DateUtils.extract_date(completed_rental.get("rent_end_date"))
                    if completed_rental.get("rent_end_date")
                    else None
                ),
            }

            return formatted_rental

        else:
            return None

    @staticmethod
    def get_user_completed_rentals_service(
        user_id: str, params: dict[str, Any]
    ) -> list[dict[str, Any]]:

        if params["sort_by"] and params["sort_by"] == "start date":
            params["sort_by"] = "rent_start_date"
        elif params["sort_by"]:
            params["sort_by"] = "rent_end_date"

        raw_completed_rentals = RentalsRepository.get_user_completed_rentals(
            user_id, params
        )

        formatted_rentals = []
        for rental in raw_completed_rentals:
            formatted_rental = {
                "rental_id": rental.get("rental_id"),
                "rent_status": rental.get("rent_status"),
                "original_owner_id": rental.get("original_owner_id"),
                "user_id": rental.get("user_id"),
                "book_id": rental.get("book_id"),
                "title": rental.get("title", ""),
                "author": rental.get("author", ""),
                "image": rental.get("image"),
                "from": rental.get("from", ""),
                "actual_deposit": rental.get("actual_deposit", 0),
                "actual_rate": rental.get("actual_rate", 0),
                "all_fees_captured": rental.get("all_fees_captured", False),
                "reserved_at": DateUtils.format_datetime_to_iso(
                    rental.get("reserved_at")
                ),
                "reservation_expires_at": DateUtils.format_datetime_to_iso(
                    rental.get("reservation_expires_at")
                ),
                "rental_duration_days": rental.get("rental_duration_days", 0),
                "meetup_location": rental.get("meetup_location", ""),
                "meetup_time_window": rental.get("meetup_time_window", ""),
                "meetup_time": rental.get("meetup_time"),
                "pickup_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    rental.get("pickup_confirmation_started_at")
                ),
                "user_confirmed_pickup": rental.get("user_confirmed_pickup", False),
                "owner_confirmed_pickup": rental.get("owner_confirmed_pickup", False),
                "return_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    rental.get("return_confirmation_started_at")
                ),
                "user_confirmed_return": rental.get("user_confirmed_return", False),
                "owner_confirmed_return": rental.get("owner_confirmed_return", False),
                "cost": (
                    int(rental.get("cost", 0))
                    if rental.get("cost") not in (None, "")
                    else 0
                ),
                "meetup_date": (
                    DateUtils.extract_date(rental.get("meetup_date"))
                    if rental.get("meetup_date")
                    else None
                ),
                "rent_start_date": (
                    DateUtils.extract_date(rental.get("rent_start_date"))
                    if rental.get("rent_start_date")
                    else None
                ),
                "rent_end_date": (
                    DateUtils.extract_date(rental.get("rent_end_date"))
                    if rental.get("rent_end_date")
                    else None
                ),
            }
            formatted_rentals.append(formatted_rental)

        return formatted_rentals

    @staticmethod
    def get_user_completed_rentals_count_service(user_id: str) -> int:

        return RentalsRepository.get_user_completed_rentals_count(user_id)["count"]

    @staticmethod
    def get_user_lendings_with_status(user_id: str) -> list[dict[str, Any]]:
        raw_lendings = RentalsRepository.get_user_lendings_with_status(user_id)

        formatted_lendings = []
        for lending in raw_lendings:
            formatted_lending = {
                "rental_id": lending.get("rental_id"),
                "rent_status": lending.get("rent_status"),
                "original_owner_id": lending.get("original_owner_id"),
                "user_id": lending.get("user_id"),
                "book_id": lending.get("book_id"),
                "title": lending.get("title", ""),
                "author": lending.get("author", ""),
                "image": lending.get("image"),
                "to": lending.get("to", ""),
                "actual_deposit": lending.get("actual_deposit", 0),
                "actual_rate": lending.get("actual_rate", 0),
                "all_fees_captured": lending.get("all_fees_captured", False),
                "reserved_at": DateUtils.format_datetime_to_iso(
                    lending.get("reserved_at")
                ),
                "reservation_expires_at": DateUtils.format_datetime_to_iso(
                    lending.get("reservation_expires_at")
                ),
                "rental_duration_days": lending.get("rental_duration_days", 0),
                "meetup_location": lending.get("meetup_location", ""),
                "meetup_time_window": lending.get("meetup_time_window", ""),
                "meetup_time": lending.get("meetup_time"),
                "pickup_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    lending.get("pickup_confirmation_started_at")
                ),
                "user_confirmed_pickup": lending.get("user_confirmed_pickup", False),
                "owner_confirmed_pickup": lending.get("owner_confirmed_pickup", False),
                "return_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    lending.get("return_confirmation_started_at")
                ),
                "user_confirmed_return": lending.get("user_confirmed_return", False),
                "owner_confirmed_return": lending.get("owner_confirmed_return", False),
                "cost": (
                    int(lending.get("cost", 0))
                    if lending.get("cost") not in (None, "")
                    else 0
                ),
                "meetup_date": (
                    DateUtils.extract_date(lending.get("meetup_date"))
                    if lending.get("meetup_date")
                    else None
                ),
                "rent_start_date": (
                    DateUtils.extract_date(lending.get("rent_start_date"))
                    if lending.get("rent_start_date")
                    else None
                ),
                "rent_end_date": (
                    DateUtils.extract_date(lending.get("rent_end_date"))
                    if lending.get("rent_end_date")
                    else None
                ),
            }
            formatted_lendings.append(formatted_lending)
        return formatted_lendings

    @staticmethod
    def get_completed_lending_service(
        user_id: str, rental_id: str
    ) -> dict[str, Any] | None:

        completed_lending = RentalsRepository.get_completed_lending(user_id, rental_id)

        if completed_lending:
            formatted_lending = {
                "rental_id": completed_lending.get("rental_id"),
                "rent_status": completed_lending.get("rent_status"),
                "original_owner_id": completed_lending.get("original_owner_id"),
                "user_id": completed_lending.get("user_id"),
                "book_id": completed_lending.get("book_id"),
                "title": completed_lending.get("title", ""),
                "author": completed_lending.get("author", ""),
                "image": completed_lending.get("image"),
                "to": completed_lending.get("to", ""),
                "actual_deposit": completed_lending.get("actual_deposit", 0),
                "actual_rate": completed_lending.get("actual_rate", 0),
                "all_fees_captured": completed_lending.get("all_fees_captured", False),
                "reserved_at": DateUtils.format_datetime_to_iso(
                    completed_lending.get("reserved_at")
                ),
                "reservation_expires_at": DateUtils.format_datetime_to_iso(
                    completed_lending.get("reservation_expires_at")
                ),
                "rental_duration_days": completed_lending.get(
                    "rental_duration_days", 0
                ),
                "meetup_location": completed_lending.get("meetup_location", ""),
                "meetup_time_window": completed_lending.get("meetup_time_window", ""),
                "meetup_time": completed_lending.get("meetup_time"),
                "pickup_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    completed_lending.get("pickup_confirmation_started_at")
                ),
                "user_confirmed_pickup": completed_lending.get(
                    "user_confirmed_pickup", False
                ),
                "owner_confirmed_pickup": completed_lending.get(
                    "owner_confirmed_pickup", False
                ),
                "return_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    completed_lending.get("return_confirmation_started_at")
                ),
                "user_confirmed_return": completed_lending.get(
                    "user_confirmed_return", False
                ),
                "owner_confirmed_return": completed_lending.get(
                    "owner_confirmed_return", False
                ),
                "cost": (
                    int(completed_lending.get("cost", 0))
                    if completed_lending.get("cost") not in (None, "")
                    else 0
                ),
                "meetup_date": (
                    DateUtils.extract_date(completed_lending.get("meetup_date"))
                    if completed_lending.get("meetup_date")
                    else None
                ),
                "rent_start_date": (
                    DateUtils.extract_date(completed_lending.get("rent_start_date"))
                    if completed_lending.get("rent_start_date")
                    else None
                ),
                "rent_end_date": (
                    DateUtils.extract_date(completed_lending.get("rent_end_date"))
                    if completed_lending.get("rent_end_date")
                    else None
                ),
            }

            return formatted_lending

        else:
            return None

    @staticmethod
    def get_user_completed_lendings_service(
        user_id: str, params: dict[str, Any]
    ) -> list[dict[str, Any]]:

        if params["sort_by"] and params["sort_by"] == "start date":
            params["sort_by"] = "rent_start_date"
        elif params["sort_by"]:
            params["sort_by"] = "rent_end_date"

        raw_completed_lendings = RentalsRepository.get_user_completed_lendings(
            user_id, params
        )

        formatted_lendings = []
        for lending in raw_completed_lendings:
            formatted_lending = {
                "rental_id": lending.get("rental_id"),
                "rent_status": lending.get("rent_status"),
                "original_owner_id": lending.get("original_owner_id"),
                "user_id": lending.get("user_id"),
                "book_id": lending.get("book_id"),
                "title": lending.get("title", ""),
                "author": lending.get("author", ""),
                "image": lending.get("image"),
                "to": lending.get("to", ""),
                "actual_deposit": lending.get("actual_deposit", 0),
                "actual_rate": lending.get("actual_rate", 0),
                "all_fees_captured": lending.get("all_fees_captured", False),
                "reserved_at": DateUtils.format_datetime_to_iso(
                    lending.get("reserved_at")
                ),
                "reservation_expires_at": DateUtils.format_datetime_to_iso(
                    lending.get("reservation_expires_at")
                ),
                "rental_duration_days": lending.get("rental_duration_days", 0),
                "meetup_location": lending.get("meetup_location", ""),
                "meetup_time_window": lending.get("meetup_time_window", ""),
                "meetup_time": lending.get("meetup_time"),
                "pickup_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    lending.get("pickup_confirmation_started_at")
                ),
                "user_confirmed_pickup": lending.get("user_confirmed_pickup", False),
                "owner_confirmed_pickup": lending.get("owner_confirmed_pickup", False),
                "return_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    lending.get("return_confirmation_started_at")
                ),
                "user_confirmed_return": lending.get("user_confirmed_return", False),
                "owner_confirmed_return": lending.get("owner_confirmed_return", False),
                "cost": (
                    int(lending.get("cost", 0))
                    if lending.get("cost") not in (None, "")
                    else 0
                ),
                "meetup_date": (
                    DateUtils.extract_date(lending.get("meetup_date"))
                    if lending.get("meetup_date")
                    else None
                ),
                "rent_start_date": (
                    DateUtils.extract_date(lending.get("rent_start_date"))
                    if lending.get("rent_start_date")
                    else None
                ),
                "rent_end_date": (
                    DateUtils.extract_date(lending.get("rent_end_date"))
                    if lending.get("rent_end_date")
                    else None
                ),
            }
            formatted_lendings.append(formatted_lending)
        return formatted_lendings

    @staticmethod
    def get_user_completed_lendings_count_service(user_id: str) -> int:

        return RentalsRepository.get_user_completed_lendings_count(user_id)["count"]

    @staticmethod
    def validate_meetup_time(meetup_time: str, time_window: str) -> tuple[bool, str]:
        """
        Validate if meetup time falls within the requested time window.

        Args:
            meetup_time (str): Time in 12-hour format (HH:MM AM/PM).
            time_window (str): Time window like "10:00 AM - 1:00 PM".

        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not time_window:
            return True, ""

        try:
            parts = time_window.split("-")
            if len(parts) != 2:
                return True, ""

            start_str = parts[0].strip()
            end_str = parts[1].strip()

            start_time = datetime.strptime(start_str, "%I:%M %p").time()
            end_time = datetime.strptime(end_str, "%I:%M %p").time()
            meetup = datetime.strptime(meetup_time, "%I:%M %p").time()

            if meetup < start_time or meetup > end_time:
                return False, f"Meetup time must be between {time_window}"

            return True, ""
        except Exception as e:
            logger.error(f"Error validating time: {e}")
            return True, ""

    @staticmethod
    def approve_rental_request(
        rental_id: str, meetup_time: str, approver_user_id: str
    ) -> tuple[dict[str, Any] | None, str | None, str | None, str | None]:
        """
        Approve a rental request with meetup time.
        This will:
        1. Check if book is still available (no other approved rentals)
        2. Set all_fees_captured to TRUE
        3. Deduct amount from reserved_amount and balance (renter)
        4. Add rental fee to owner's wallet
        5. Create transaction logs for both users
        """
        try:
            if not meetup_time:
                return None, "Meetup time is required", None, None

            # Convert 24-hour format to 12-hour format
            meetup_time_12hour = DateUtils.convert_to_12_hour_format(meetup_time)

            # Get rental details
            rental = RentalsRepository.get_rental_by_id(rental_id)

            if not rental:
                return None, "Rental not found", None, None

            owner_id = rental.get("owner_id")
            rent_status = rental.get("rent_status")
            time_window = rental.get("meetup_time_window", "")
            renter_user_id = rental.get("user_id")
            total_cost = int(rental.get("total_rent_cost", 0))

            # Verify the approver is the owner
            if str(owner_id) != str(approver_user_id):
                return (
                    None,
                    "Unauthorized: Only the book owner can approve this rental",
                    None,
                    None,
                )

            # Check if rental is in pending status
            if rent_status != "pending":
                return (
                    None,
                    f"Rental cannot be approved. Current status: {rent_status}",
                    None,
                    None,
                )

            book_id = RentalsRepository.get_book_id_from_rental(rental_id)
            if book_id:
                active_rental = RentalsRepository.check_book_availability(
                    book_id, str(owner_id)
                )
                if active_rental:
                    renter_name = active_rental.get("renter_username", "another user")
                    return (
                        None,
                        f"This book is already approved for rental to {renter_name}. Please reject other pending requests first.",
                        None,
                        None,
                    )

            # Validate meetup time against time window
            is_valid, error_msg = RentalsServices.validate_meetup_time(
                meetup_time_12hour, time_window
            )

            if not is_valid:
                return None, error_msg, None, None

            # Ensure renter_user_id is a string
            if not renter_user_id:
                return None, "Renter user ID not found", None, None
            renter_user_id_str = str(renter_user_id)
            owner_user_id_str = str(owner_id)

            # Deduct from renter's reserved_amount and balance
            wallet_result = WalletRepository.deduct_from_reserved_and_balance(
                renter_user_id_str, total_cost
            )

            if not wallet_result:
                return None, "Insufficient funds or wallet not found", None, None

            renter_wallet_id = wallet_result.get("wallet_id")

            # Ensure wallet_id is a string
            if not renter_wallet_id:
                return None, "Wallet ID not found after deduction", None, None
            renter_wallet_id_str = str(renter_wallet_id)

            # Add rental fee to owner's wallet
            owner_wallet_result = WalletRepository.add_rental_fee_to_owner(
                owner_user_id_str, total_cost
            )

            if not owner_wallet_result:
                logger.error(
                    f"Failed to add rental fee to owner wallet for rental {rental_id}"
                )
                return None, "Failed to credit owner's wallet", None, None

            owner_wallet_id = str(owner_wallet_result.get("wallet_id"))

            # Create transaction log for renter (deduction)
            renter_transaction = WalletRepository.insert_transaction(
                wallet_id=renter_wallet_id_str,
                amount=-total_cost,
                transaction_type="rent",
            )

            # Create transaction log for owner (credit)
            owner_transaction = WalletRepository.insert_transaction(
                wallet_id=owner_wallet_id,
                amount=total_cost,
                transaction_type="rent",
            )

            if not renter_transaction:
                logger.error(
                    f"Failed to create renter transaction log for rental {rental_id}"
                )

            if not owner_transaction:
                logger.error(
                    f"Failed to create owner transaction log for rental {rental_id}"
                )

            # Approve the rental with 12-hour format time
            result = RentalsRepository.approve_rental(rental_id, meetup_time_12hour)

            if not result:
                return None, "Failed to update rental status", None, None

            logger.info(
                f"Rental {rental_id} approved. "
                f"Deducted {total_cost} from renter {renter_user_id_str}. "
                f"Added {total_cost} to owner {owner_user_id_str}. "
                f"Renter transaction: {renter_transaction.get('transaction_id') if renter_transaction else 'N/A'}, "
                f"Owner transaction: {owner_transaction.get('transaction_id') if owner_transaction else 'N/A'}"
            )

            return result, None, book_id, renter_user_id

        except Exception as e:
            logger.error(f"Error in approve_rental_request: {str(e)}")
            traceback.print_exc()
            return None, f"Error: {str(e)}", None, None

    @staticmethod
    def reject_rental_request(
        rental_id: str, reason: str, rejecter_user_id: str
    ) -> tuple[dict[str, Any] | None, str | None, str | None]:
        """
        Reject a rental request.
        This will:
        1. Delete the rental entry from rented_books
        2. Deduct the total_cost from the renter's reserved_amount
        """
        try:
            rental = RentalsRepository.get_rental_by_id(rental_id)

            if not rental:
                return None, "Rental not found", None

            owner_id = rental.get("owner_id")
            rent_status = rental.get("rent_status")
            renter_user_id = rental.get("user_id")
            total_cost = int(rental.get("total_rent_cost", 0))

            # Verify the rejecter is the owner
            if str(owner_id) != str(rejecter_user_id):
                return (
                    None,
                    "Unauthorized: Only the book owner can reject this rental",
                    None,
                )

            if rent_status != "pending":
                return (
                    None,
                    f"Rental cannot be rejected. Current status: {rent_status}",
                    None,
                )

            if not renter_user_id:
                return None, "Renter user ID not found", None
            renter_user_id_str = str(renter_user_id)

            wallet_result = WalletRepository.deduct_from_reserved_amount(
                renter_user_id_str, total_cost
            )

            if not wallet_result:
                logger.warning(
                    f"Failed to release reserved funds for rental {rental_id}. "
                    f"User: {renter_user_id_str}, Amount: {total_cost}"
                )
                # Continue with deletion even if wallet update fails

            logger.info(
                f"Rental {rental_id} rejected by owner {rejecter_user_id}. "
                f"Reason: {reason}. "
                f"Released {total_cost} from reserved_amount for user {renter_user_id_str}. "
                f"Rental entry deleted."
            )

            return (
                {
                    "rental_id": rental_id,
                    "reason": reason,
                    "released_amount": total_cost,
                },
                None,
                renter_user_id,
            )

        except Exception as e:
            logger.error(f"Error in reject_rental_request: {str(e)}")
            return None, f"Error: {str(e)}", None

    @staticmethod
    def cancel_rental_request(
        rental_id: str, canceller_user_id: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Cancel a rental request by the renter.
        This will:
        1. Delete the rental entry from rented_books
        2. Deduct the total_cost from the renter's reserved_amount
        """
        try:
            rental = RentalsRepository.get_rental_by_id(rental_id)

            if not rental:
                return None, "Rental not found"

            renter_user_id = rental.get("user_id")
            rent_status = rental.get("rent_status")
            total_cost = int(rental.get("total_rent_cost", 0))

            # Verify the canceller is the renter
            if str(renter_user_id) != str(canceller_user_id):
                return None, "Unauthorized: Only the renter can cancel this rental"

            if rent_status != "pending":
                return (
                    None,
                    f"Rental cannot be cancelled. Current status: {rent_status}",
                )

            if not renter_user_id:
                return None, "Renter user ID not found"
            renter_user_id_str = str(renter_user_id)

            wallet_result = WalletRepository.deduct_from_reserved_amount(
                renter_user_id_str, total_cost
            )

            if not wallet_result:
                logger.warning(
                    f"Failed to release reserved funds for rental {rental_id}. "
                    f"User: {renter_user_id_str}, Amount: {total_cost}"
                )
                # Continue with deletion even if wallet update fails

            logger.info(
                f"Rental {rental_id} cancelled by renter {canceller_user_id}. "
                f"Released {total_cost} from reserved_amount for user {renter_user_id_str}. "
                f"Rental entry deleted."
            )

            return {
                "rental_id": rental_id,
                "released_amount": total_cost,
            }, None

        except Exception as e:
            logger.error(f"Error in cancel_rental_request: {str(e)}")
            return None, f"Error: {str(e)}"

    @staticmethod
    def create_rental_service(rental_data: dict[str, Any]) -> dict[str, Any] | None:
        """
        Create a new rental request in the database.

        Args:
            rental_data (dict): A dictionary containing rental details:
            - user_id
            - book_id
            - reserved_at
            - reservation_expires_at
            - total_rent_cost
            - rental_duration_days
            - meetup_time_window
            - meetup_location
            - meetup_date
            - original_user_id

        Returns:
            dict: The inserted rental record if successful, None otherwise.
        """
        try:
            rental = RentalsRepository.insert_rental(rental_data)
            if not rental:
                return None
            return rental
        except Exception:
            traceback.print_exc()
            return None

    @staticmethod
    def check_pending_rental(user_id: str, book_id: str) -> bool:
        """
        Check if the user already has a pending rental for the given book.

        Returns:
            bool: True if a pending rental exists, False otherwise.
        """
        try:
            return RentalsRepository.exists_pending_rental(user_id, book_id)
        except Exception:
            traceback.print_exc()
            return False

    @staticmethod
    def confirm_pickup(
        rental_id: str, confirmer_user_id: str
    ) -> tuple[dict[str, Any] | None, str | None, str | None, str | None]:
        """
        Confirm book pickup by either the renter or owner.
        When both confirm, move to 'ongoing' status and set rent_start_date.
        """
        try:
            rental = RentalsRepository.get_rental_by_id_full(rental_id)

            if not rental:
                return None, "Rental not found", None, None

            owner_id = rental.get("owner_id")
            renter_user_id = rental.get("user_id")
            rent_status = rental.get("rent_status")
            user_confirmed = rental.get("user_confirmed_pickup", False)
            owner_confirmed = rental.get("owner_confirmed_pickup", False)
            rental_duration = rental.get("rental_duration_days", 0)

            # Check if rental is in correct status
            if rent_status != "awaiting_pickup_confirmation":
                return (
                    None,
                    f"Cannot confirm pickup. Current status: {rent_status}",
                    None,
                    None,
                )

            # Determine if confirmer is owner or renter
            is_owner = str(owner_id) == str(confirmer_user_id)
            is_renter = str(renter_user_id) == str(confirmer_user_id)

            if not is_owner and not is_renter:
                return (
                    None,
                    "Unauthorized: Only the renter or owner can confirm pickup",
                    None,
                    None,
                )

            # Update confirmation status
            if is_owner and owner_confirmed:
                return None, "You have already confirmed pickup", None, None
            if is_renter and user_confirmed:
                return None, "You have already confirmed pickup", None, None

            # Confirm pickup
            result = RentalsRepository.confirm_pickup(
                rental_id, is_owner, is_renter, rental_duration
            )

            if not result:
                return None, "Failed to confirm pickup", None, None

            logger.info(
                f"Pickup confirmed for rental {rental_id} by "
                f"{'owner' if is_owner else 'renter'} {confirmer_user_id}"
            )

            return result, None, owner_id, renter_user_id

        except Exception as e:
            logger.error(f"Error in confirm_pickup: {str(e)}")
            return None, f"Error: {str(e)}", None, None

    @staticmethod
    def confirm_return(
        rental_id: str, confirmer_user_id: str
    ) -> tuple[dict[str, Any] | None, str | None, str | None, str | None]:
        """
        Confirm book return by either the renter or owner.
        When both confirm, move to 'completed' status and return security deposit.
        """
        try:
            rental = RentalsRepository.get_rental_by_id_full_return(rental_id)

            if not rental:
                return None, "Rental not found", None, None

            owner_id = rental.get("owner_id")
            renter_user_id = rental.get("user_id")
            rent_status = rental.get("rent_status")
            user_confirmed = rental.get("user_confirmed_return", False)
            owner_confirmed = rental.get("owner_confirmed_return", False)

            # Check if rental is in correct status
            if rent_status != "awaiting_return_confirmation":
                return (
                    None,
                    f"Cannot confirm return. Current status: {rent_status}",
                    None,
                    None,
                )

            # Determine if confirmer is owner or renter
            is_owner = str(owner_id) == str(confirmer_user_id)
            is_renter = str(renter_user_id) == str(confirmer_user_id)

            if not is_owner and not is_renter:
                return (
                    None,
                    "Unauthorized: Only the renter or owner can confirm return",
                    None,
                    None,
                )

            # Update confirmation status
            if is_owner and owner_confirmed:
                return None, "You have already confirmed return", None, None
            if is_renter and user_confirmed:
                return None, "You have already confirmed return", None, None

            # Confirm return
            result = RentalsRepository.confirm_return(rental_id, is_owner, is_renter)

            if not result:
                return None, "Failed to confirm return", None, None

            # Check if both users have now confirmed (status changed to 'rate_user')
            new_status = result.get("rent_status")

            if new_status == "completed":
                # Both users confirmed - return security deposit
                actual_deposit = result.get("actual_deposit", 0)
                renter_id = str(result.get("user_id"))
                owner_id_str = str(result.get("owner_id"))

                if actual_deposit > 0:
                    # Return deposit from owner to renter
                    renter_wallet, owner_wallet = (
                        WalletRepository.return_security_deposit(
                            renter_id, owner_id_str, actual_deposit
                        )
                    )

                    if not renter_wallet or not owner_wallet:
                        logger.error(
                            f"Failed to return security deposit for rental {rental_id}. "
                            f"Deposit amount: {actual_deposit}"
                        )
                        return (
                            None,
                            "Failed to return security deposit. Owner may have insufficient funds.",
                            None,
                            None,
                        )

                    # Create transaction logs
                    renter_wallet_id = str(renter_wallet.get("wallet_id"))
                    owner_wallet_id = str(owner_wallet.get("wallet_id"))

                    # Positive transaction for renter (receiving deposit back)
                    renter_transaction = WalletRepository.insert_deposit_transaction(
                        renter_wallet_id, actual_deposit, "deposit_received"
                    )

                    # Negative transaction for owner (returning deposit)
                    owner_transaction = WalletRepository.insert_deposit_transaction(
                        owner_wallet_id, -actual_deposit, "deposit_returned"
                    )

                    if not renter_transaction or not owner_transaction:
                        logger.warning(
                            f"Security deposit returned but failed to create transaction logs "
                            f"for rental {rental_id}"
                        )

                    logger.info(
                        f"Security deposit of {actual_deposit} returned for rental {rental_id}. "
                        f"From owner {owner_id_str} to renter {renter_id}. "
                        f"Renter transaction (deposit_received): "
                        f"{renter_transaction.get('transaction_id') if renter_transaction else 'N/A'}, "
                        f"Owner transaction (deposit_returned): "
                        f"{owner_transaction.get('transaction_id') if owner_transaction else 'N/A'}"
                    )

            logger.info(
                f"Return confirmed for rental {rental_id} by "
                f"{'owner' if is_owner else 'renter'} {confirmer_user_id}"
            )

            return result, None, owner_id, renter_user_id

        except Exception as e:
            logger.error(f"Error in confirm_return: {str(e)}")
            traceback.print_exc()
            return None, f"Error: {str(e)}", None, None

    @staticmethod
    def get_rental_details_for_pickup(rental_id: str) -> dict[str, Any] | None:
        """Get the details of a rental from a rental_id"""

        return RentalsRepository.get_rental_by_id_full(rental_id)
