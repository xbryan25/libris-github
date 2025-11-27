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
                "book_id": rental.get("book_id"),
                "title": rental.get("title", ""),
                "author": rental.get("author", ""),
                "image": rental.get("image"),
                "from": rental.get("from", ""),
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
    def get_user_lendings_with_status(user_id: str) -> list[dict[str, Any]]:
        raw_lendings = RentalsRepository.get_user_lendings_with_status(user_id)

        formatted_lendings = []
        for lending in raw_lendings:
            formatted_lending = {
                "rental_id": lending.get("rental_id"),
                "rent_status": lending.get("rent_status"),
                "book_id": lending.get("book_id"),
                "title": lending.get("title", ""),
                "author": lending.get("author", ""),
                "image": lending.get("image"),
                "to": lending.get("to", ""),
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
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Approve a rental request with meetup time.
        This will:
        1. Set all_fees_captured to TRUE
        2. Deduct amount from reserved_amount and balance
        3. Create transaction log
        """
        try:
            if not meetup_time:
                return None, "Meetup time is required"

            # Convert 24-hour format to 12-hour format
            meetup_time_12hour = DateUtils.convert_to_12_hour_format(meetup_time)

            # Get rental details
            rental = RentalsRepository.get_rental_by_id(rental_id)

            if not rental:
                return None, "Rental not found"

            owner_id = rental.get("owner_id")
            rent_status = rental.get("rent_status")
            time_window = rental.get("meetup_time_window", "")
            renter_user_id = rental.get("user_id")
            total_cost = int(rental.get("total_rent_cost", 0))

            # Verify the approver is the owner
            if str(owner_id) != str(approver_user_id):
                return None, "Unauthorized: Only the book owner can approve this rental"

            # Check if rental is in pending status
            if rent_status != "pending":
                return None, f"Rental cannot be approved. Current status: {rent_status}"

            # Validate meetup time against time window
            is_valid, error_msg = RentalsServices.validate_meetup_time(
                meetup_time_12hour, time_window
            )

            if not is_valid:
                return None, error_msg

            # Ensure renter_user_id is a string
            if not renter_user_id:
                return None, "Renter user ID not found"
            renter_user_id_str = str(renter_user_id)

            # Deduct from reserved_amount and balance
            wallet_result = WalletRepository.deduct_from_reserved_and_balance(
                renter_user_id_str, total_cost
            )

            if not wallet_result:
                return None, "Insufficient funds or wallet not found"

            wallet_id = wallet_result.get("wallet_id")

            # Ensure wallet_id is a string
            if not wallet_id:
                return None, "Wallet ID not found after deduction"
            wallet_id_str = str(wallet_id)

            # Create transaction log
            transaction_result = WalletRepository.insert_transaction(
                wallet_id=wallet_id_str,
                amount=-total_cost,  # Negative because it's a deduction
                transaction_type="rent",
            )

            if not transaction_result:
                logger.error(f"Failed to create transaction log for rental {rental_id}")
                # Note: The wallet deduction already happened, so we log but don't fail

            # Approve the rental with 12-hour format time
            result = RentalsRepository.approve_rental(rental_id, meetup_time_12hour)

            if not result:
                return None, "Failed to update rental status"

            logger.info(
                f"Rental {rental_id} approved. "
                f"Deducted {total_cost} from user {renter_user_id_str}. "
                f"Transaction ID: {transaction_result.get('transaction_id') if transaction_result else 'N/A'}"
            )

            return result, None

        except Exception as e:
            logger.error(f"Error in approve_rental_request: {str(e)}")
            return None, f"Error: {str(e)}"

    @staticmethod
    def reject_rental_request(
        rental_id: str, reason: str, rejecter_user_id: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Reject a rental request.
        This will:
        1. Delete the rental entry from rented_books
        2. Deduct the total_cost from the renter's reserved_amount
        """
        try:
            rental = RentalsRepository.get_rental_by_id(rental_id)

            if not rental:
                return None, "Rental not found"

            owner_id = rental.get("owner_id")
            rent_status = rental.get("rent_status")
            renter_user_id = rental.get("user_id")
            total_cost = int(rental.get("total_rent_cost", 0))

            # Verify the rejecter is the owner
            if str(owner_id) != str(rejecter_user_id):
                return None, "Unauthorized: Only the book owner can reject this rental"

            if rent_status != "pending":
                return None, f"Rental cannot be rejected. Current status: {rent_status}"

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

            # Delete the rental entry
            delete_result = RentalsRepository.delete_rental(rental_id)

            if not delete_result:
                return None, "Failed to delete rental entry"

            logger.info(
                f"Rental {rental_id} rejected by owner {rejecter_user_id}. "
                f"Reason: {reason}. "
                f"Released {total_cost} from reserved_amount for user {renter_user_id_str}. "
                f"Rental entry deleted."
            )

            return {
                "rental_id": rental_id,
                "reason": reason,
                "released_amount": total_cost,
            }, None

        except Exception as e:
            logger.error(f"Error in reject_rental_request: {str(e)}")
            return None, f"Error: {str(e)}"

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

            delete_result = RentalsRepository.delete_rental(rental_id)

            if not delete_result:
                return None, "Failed to delete rental entry"

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
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Confirm book pickup by either the renter or owner.
        When both confirm, move to 'ongoing' status and set rent_start_date.
        """
        try:
            rental = RentalsRepository.get_rental_by_id_full(rental_id)

            if not rental:
                return None, "Rental not found"

            owner_id = rental.get("owner_id")
            renter_user_id = rental.get("user_id")
            rent_status = rental.get("rent_status")
            user_confirmed = rental.get("user_confirmed_pickup", False)
            owner_confirmed = rental.get("owner_confirmed_pickup", False)
            rental_duration = rental.get("rental_duration_days", 0)

            # Check if rental is in correct status
            if rent_status != "awaiting_pickup_confirmation":
                return None, f"Cannot confirm pickup. Current status: {rent_status}"

            # Determine if confirmer is owner or renter
            is_owner = str(owner_id) == str(confirmer_user_id)
            is_renter = str(renter_user_id) == str(confirmer_user_id)

            if not is_owner and not is_renter:
                return None, "Unauthorized: Only the renter or owner can confirm pickup"

            # Update confirmation status
            if is_owner and owner_confirmed:
                return None, "You have already confirmed pickup"
            if is_renter and user_confirmed:
                return None, "You have already confirmed pickup"

            # Confirm pickup
            result = RentalsRepository.confirm_pickup(
                rental_id, is_owner, is_renter, rental_duration
            )

            if not result:
                return None, "Failed to confirm pickup"

            logger.info(
                f"Pickup confirmed for rental {rental_id} by "
                f"{'owner' if is_owner else 'renter'} {confirmer_user_id}"
            )

            return result, None

        except Exception as e:
            logger.error(f"Error in confirm_pickup: {str(e)}")
            return None, f"Error: {str(e)}"
