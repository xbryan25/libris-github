from .repository import RentalRepository
from app.features.wallets.repository import WalletRepository
from typing import Any
from app.utils import DateUtils
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RentalServices:
    @staticmethod
    def get_user_rentals_with_status(user_id: str) -> list[dict[str, Any]]:
        raw_rentals = RentalRepository.get_user_rentals_with_status(user_id)

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
                "reserved_at": rental.get("reserved_at"),
                "reservation_expires_at": rental.get("reservation_expires_at"),
                "rental_duration_days": rental.get("rental_duration_days", 0),
                "meetup_location": rental.get("meetup_location", ""),
                "meetup_time_window": rental.get("meetup_time_window", ""),
                "meetup_time": rental.get("meetup_time"),
                "pickup_confirmation_started_at": rental.get(
                    "pickup_confirmation_started_at"
                ),
                "user_confirmed_pickup": rental.get("user_confirmed_pickup", False),
                "owner_confirmed_pickup": rental.get("owner_confirmed_pickup", False),
                "return_confirmation_started_at": rental.get(
                    "return_confirmation_started_at"
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
        raw_lendings = RentalRepository.get_user_lendings_with_status(user_id)

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
                "reserved_at": lending.get("reserved_at"),
                "reservation_expires_at": lending.get("reservation_expires_at"),
                "rental_duration_days": lending.get("rental_duration_days", 0),
                "meetup_location": lending.get("meetup_location", ""),
                "meetup_time_window": lending.get("meetup_time_window", ""),
                "meetup_time": lending.get("meetup_time"),
                "pickup_confirmation_started_at": lending.get(
                    "pickup_confirmation_started_at"
                ),
                "user_confirmed_pickup": lending.get("user_confirmed_pickup", False),
                "owner_confirmed_pickup": lending.get("owner_confirmed_pickup", False),
                "return_confirmation_started_at": lending.get(
                    "return_confirmation_started_at"
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
            rental = RentalRepository.get_rental_by_id(rental_id)

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
            is_valid, error_msg = RentalServices.validate_meetup_time(
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
            result = RentalRepository.approve_rental(rental_id, meetup_time_12hour)

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
