from .repository import PurchasesRepository
from app.features.wallets.repository import WalletRepository
from typing import Any
from app.utils import DateUtils
from datetime import datetime
import logging
import traceback

logger = logging.getLogger(__name__)


class PurchasesServices:

    @staticmethod
    def create_purchase_service(purchase_data: dict[str, Any]) -> dict[str, Any] | None:
        """
        Create a new purchase record in the database.

        Args:
            purchase_data (dict): Dictionary containing purchase details:
                - user_id
                - book_id
                - reserved_at
                - reservation_expires_at
                - total_buy_cost
                - meetup_time_window
                - meetup_location
                - meetup_date

        Returns:
            dict: The inserted purchase record if successful, None otherwise.
        """
        try:
            purchase = PurchasesRepository.insert_purchase(purchase_data)
            if not purchase:
                return None
            return purchase
        except Exception:
            traceback.print_exc()
            return None

    @staticmethod
    def check_pending_purchase(user_id: str, book_id: str) -> bool:
        """
        Check if the user already has a pending purchase for the given book.

        Returns:
            bool: True if a pending purchase exists, False otherwise.
        """
        try:
            return PurchasesRepository.exists_pending_purchase(user_id, book_id)
        except Exception:
            traceback.print_exc()
            return False

    @staticmethod
    def get_user_purchases_with_status(user_id: str) -> list[dict[str, Any]]:
        raw_purchases = PurchasesRepository.get_user_purchases_with_status(user_id)

        formatted_purchases = []
        for purchase in raw_purchases:
            formatted_purchase = {
                "purchase_id": purchase.get("purchase_id"),
                "purchase_status": purchase.get("purchase_status"),
                "book_id": purchase.get("book_id"),
                "title": purchase.get("title", ""),
                "author": purchase.get("author", ""),
                "image": purchase.get("image"),
                "from": purchase.get("from", ""),
                "all_fees_captured": purchase.get("all_fees_captured", False),
                "reserved_at": DateUtils.format_datetime_to_iso(
                    purchase.get("reserved_at")
                ),
                "reservation_expires_at": DateUtils.format_datetime_to_iso(
                    purchase.get("reservation_expires_at")
                ),
                "meetup_location": purchase.get("meetup_location", ""),
                "meetup_time_window": purchase.get("meetup_time_window", ""),
                "meetup_time": purchase.get("meetup_time"),
                "pickup_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    purchase.get("pickup_confirmation_started_at")
                ),
                "user_confirmed_pickup": purchase.get("user_confirmed_pickup", False),
                "owner_confirmed_pickup": purchase.get("owner_confirmed_pickup", False),
                "user_rated": purchase.get("user_rated", False),
                "owner_rated": purchase.get("owner_rated", False),
                "transfer_decision_pending": purchase.get(
                    "transfer_decision_pending", False
                ),
                "ownership_transferred": purchase.get("ownership_transferred"),
                "cost": (
                    int(purchase.get("cost", 0))
                    if purchase.get("cost") not in (None, "")
                    else 0
                ),
                "meetup_date": (
                    DateUtils.extract_date(purchase.get("meetup_date"))
                    if purchase.get("meetup_date")
                    else None
                ),
            }
            formatted_purchases.append(formatted_purchase)

        return formatted_purchases

    @staticmethod
    def get_user_sales_with_status(user_id: str) -> list[dict[str, Any]]:
        raw_sales = PurchasesRepository.get_user_sales_with_status(user_id)

        formatted_sales = []
        for sale in raw_sales:
            formatted_sale = {
                "purchase_id": sale.get("purchase_id"),
                "purchase_status": sale.get("purchase_status"),
                "book_id": sale.get("book_id"),
                "title": sale.get("title", ""),
                "author": sale.get("author", ""),
                "image": sale.get("image"),
                "to": sale.get("to", ""),
                "all_fees_captured": sale.get("all_fees_captured", False),
                "reserved_at": DateUtils.format_datetime_to_iso(
                    sale.get("reserved_at")
                ),
                "reservation_expires_at": DateUtils.format_datetime_to_iso(
                    sale.get("reservation_expires_at")
                ),
                "meetup_location": sale.get("meetup_location", ""),
                "meetup_time_window": sale.get("meetup_time_window", ""),
                "meetup_time": sale.get("meetup_time"),
                "pickup_confirmation_started_at": DateUtils.format_datetime_to_iso(
                    sale.get("pickup_confirmation_started_at")
                ),
                "user_confirmed_pickup": sale.get("user_confirmed_pickup", False),
                "owner_confirmed_pickup": sale.get("owner_confirmed_pickup", False),
                "user_rated": sale.get("user_rated", False),
                "owner_rated": sale.get("owner_rated", False),
                "transfer_decision_pending": sale.get(
                    "transfer_decision_pending", False
                ),
                "ownership_transferred": sale.get("ownership_transferred", False),
                "cost": (
                    int(sale.get("cost", 0))
                    if sale.get("cost") not in (None, "")
                    else 0
                ),
                "meetup_date": (
                    DateUtils.extract_date(sale.get("meetup_date"))
                    if sale.get("meetup_date")
                    else None
                ),
            }
            formatted_sales.append(formatted_sale)
        return formatted_sales

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
    def approve_purchase_request(
        purchase_id: str, meetup_time: str, approver_user_id: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Approve a purchase request with meetup time.
        This will:
        1. Check if book is still available (no other approved purchases)
        2. Set all_fees_captured to TRUE
        3. Deduct amount from reserved_amount and balance (buyer)
        4. Add purchase fee to owner's wallet
        5. Create transaction logs for both users
        """
        try:
            if not meetup_time:
                return None, "Meetup time is required"

            # Convert 24-hour format to 12-hour format
            meetup_time_12hour = DateUtils.convert_to_12_hour_format(meetup_time)

            # Get purchase details
            purchase = PurchasesRepository.get_purchase_by_id(purchase_id)

            if not purchase:
                return None, "Purchase not found"

            original_owner_id = purchase.get("original_owner_id")
            purchase_status = purchase.get("purchase_status")
            time_window = purchase.get("meetup_time_window", "")
            buyer_user_id = purchase.get("user_id")
            total_cost = int(purchase.get("total_buy_cost", 0))

            # Verify the approver is the owner
            if str(original_owner_id) != str(approver_user_id):
                return (
                    None,
                    "Unauthorized: Only the book owner can approve this purchase",
                )

            # Check if purchase is in pending status
            if purchase_status != "pending":
                return (
                    None,
                    f"Purchase cannot be approved. Current status: {purchase_status}",
                )

            book_id = PurchasesRepository.get_book_id_from_purchase(purchase_id)
            if book_id:
                active_purchase = PurchasesRepository.check_book_availability(
                    book_id, str(original_owner_id)
                )
                if active_purchase:
                    buyer_name = active_purchase.get("buyer_username", "another user")
                    return (
                        None,
                        f"This book is already approved for purchase to {buyer_name}."
                        f"Please reject other pending requests first.",
                    )

            # Validate meetup time against time window
            is_valid, error_msg = PurchasesServices.validate_meetup_time(
                meetup_time_12hour, time_window
            )

            if not is_valid:
                return None, error_msg

            # Ensure buyer_user_id is a string
            if not buyer_user_id:
                return None, "Buyer user ID not found"
            buyer_user_id_str = str(buyer_user_id)
            owner_user_id_str = str(original_owner_id)

            # Deduct from buyer's reserved_amount and balance
            wallet_result = WalletRepository.deduct_from_reserved_and_balance(
                buyer_user_id_str, total_cost
            )

            if not wallet_result:
                return None, "Insufficient funds or wallet not found"

            buyer_wallet_id = wallet_result.get("wallet_id")

            # Ensure wallet_id is a string
            if not buyer_wallet_id:
                return None, "Wallet ID not found after deduction"
            buyer_wallet_id_str = str(buyer_wallet_id)

            # Add purchase fee to owner's wallet
            owner_wallet_result = WalletRepository.add_rental_fee_to_owner(
                owner_user_id_str, total_cost
            )

            if not owner_wallet_result:
                logger.error(
                    f"Failed to add purchase fee to owner wallet for purchase {purchase_id}"
                )
                return None, "Failed to credit owner's wallet"

            owner_wallet_id = str(owner_wallet_result.get("wallet_id"))

            # Create transaction log for buyer (deduction)
            buyer_transaction = WalletRepository.insert_transaction(
                wallet_id=buyer_wallet_id_str,
                amount=-total_cost,
                transaction_type="purchase",
            )

            # Create transaction log for owner (credit)
            owner_transaction = WalletRepository.insert_transaction(
                wallet_id=owner_wallet_id,
                amount=total_cost,
                transaction_type="sale",
            )

            if not buyer_transaction:
                logger.error(
                    f"Failed to create buyer transaction log for purchase {purchase_id}"
                )

            if not owner_transaction:
                logger.error(
                    f"Failed to create owner transaction log for purchase {purchase_id}"
                )

            # Approve the purchase with 12-hour format time
            result = PurchasesRepository.approve_purchase(
                purchase_id, meetup_time_12hour
            )

            if not result:
                return None, "Failed to update purchase status"

            logger.info(
                f"Purchase {purchase_id} approved. "
                f"Deducted {total_cost} from buyer {buyer_user_id_str}. "
                f"Added {total_cost} to owner {owner_user_id_str}. "
                f"Buyer transaction: {buyer_transaction.get('transaction_id') if buyer_transaction else 'N/A'}, "
                f"Owner transaction: {owner_transaction.get('transaction_id') if owner_transaction else 'N/A'}"
            )

            return result, None

        except Exception as e:
            logger.error(f"Error in approve_purchase_request: {str(e)}")
            traceback.print_exc()
            return None, f"Error: {str(e)}"

    @staticmethod
    def reject_purchase_request(
        purchase_id: str, reason: str, rejecter_user_id: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Reject a purchase request.
        This will:
        1. Delete the purchase entry from purchased_books
        2. Deduct the total_cost from the buyer's reserved_amount
        """
        try:
            purchase = PurchasesRepository.get_purchase_by_id(purchase_id)

            if not purchase:
                return None, "Purchase not found"

            original_owner_id = purchase.get("original_owner_id")
            purchase_status = purchase.get("purchase_status")
            buyer_user_id = purchase.get("user_id")
            total_cost = int(purchase.get("total_buy_cost", 0))

            # Verify the rejecter is the owner
            if str(original_owner_id) != str(rejecter_user_id):
                return (
                    None,
                    "Unauthorized: Only the book owner can reject this purchase",
                )

            if purchase_status != "pending":
                return (
                    None,
                    f"Purchase cannot be rejected. Current status: {purchase_status}",
                )

            if not buyer_user_id:
                return None, "Buyer user ID not found"
            buyer_user_id_str = str(buyer_user_id)

            wallet_result = WalletRepository.deduct_from_reserved_amount(
                buyer_user_id_str, total_cost
            )

            if not wallet_result:
                logger.warning(
                    f"Failed to release reserved funds for purchase {purchase_id}. "
                    f"User: {buyer_user_id_str}, Amount: {total_cost}"
                )

            # Delete the purchase entry
            delete_result = PurchasesRepository.delete_purchase(purchase_id)

            if not delete_result:
                return None, "Failed to delete purchase entry"

            logger.info(
                f"Purchase {purchase_id} rejected by owner {rejecter_user_id}. "
                f"Reason: {reason}. "
                f"Released {total_cost} from reserved_amount for user {buyer_user_id_str}. "
                f"Purchase entry deleted."
            )

            return {
                "purchase_id": purchase_id,
                "reason": reason,
                "released_amount": total_cost,
            }, None

        except Exception as e:
            logger.error(f"Error in reject_purchase_request: {str(e)}")
            return None, f"Error: {str(e)}"

    @staticmethod
    def cancel_purchase_request(
        purchase_id: str, canceller_user_id: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Cancel a purchase request by the buyer.
        This will:
        1. Delete the purchase entry from purchased_books
        2. Deduct the total_cost from the buyer's reserved_amount
        """
        try:
            purchase = PurchasesRepository.get_purchase_by_id(purchase_id)

            if not purchase:
                return None, "Purchase not found"

            buyer_user_id = purchase.get("user_id")
            purchase_status = purchase.get("purchase_status")
            total_cost = int(purchase.get("total_buy_cost", 0))

            # Verify the canceller is the buyer
            if str(buyer_user_id) != str(canceller_user_id):
                return None, "Unauthorized: Only the buyer can cancel this purchase"

            if purchase_status != "pending":
                return (
                    None,
                    f"Purchase cannot be cancelled. Current status: {purchase_status}",
                )

            if not buyer_user_id:
                return None, "Buyer user ID not found"
            buyer_user_id_str = str(buyer_user_id)

            wallet_result = WalletRepository.deduct_from_reserved_amount(
                buyer_user_id_str, total_cost
            )

            if not wallet_result:
                logger.warning(
                    f"Failed to release reserved funds for purchase {purchase_id}. "
                    f"User: {buyer_user_id_str}, Amount: {total_cost}"
                )

            delete_result = PurchasesRepository.delete_purchase(purchase_id)

            if not delete_result:
                return None, "Failed to delete purchase entry"

            logger.info(
                f"Purchase {purchase_id} cancelled by buyer {canceller_user_id}. "
                f"Released {total_cost} from reserved_amount for user {buyer_user_id_str}. "
                f"Purchase entry deleted."
            )

            return {
                "purchase_id": purchase_id,
                "released_amount": total_cost,
            }, None

        except Exception as e:
            logger.error(f"Error in cancel_purchase_request: {str(e)}")
            return None, f"Error: {str(e)}"

    @staticmethod
    def confirm_pickup(
        purchase_id: str, confirmer_user_id: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Confirm book pickup by either the buyer or owner.
        When both confirm, move to 'completed' status.
        """
        try:
            purchase = PurchasesRepository.get_purchase_by_id_full(purchase_id)

            if not purchase:
                return None, "Purchase not found"

            original_owner_id = purchase.get("original_owner_id")
            buyer_user_id = purchase.get("user_id")
            purchase_status = purchase.get("purchase_status")
            user_confirmed = purchase.get("user_confirmed_pickup", False)
            owner_confirmed = purchase.get("owner_confirmed_pickup", False)

            # Check if purchase is in correct status
            if purchase_status != "awaiting_pickup_confirmation":
                return None, f"Cannot confirm pickup. Current status: {purchase_status}"

            # Determine if confirmer is owner or buyer
            is_owner = str(original_owner_id) == str(confirmer_user_id)
            is_buyer = str(buyer_user_id) == str(confirmer_user_id)

            if not is_owner and not is_buyer:
                return None, "Unauthorized: Only the buyer or owner can confirm pickup"

            # Update confirmation status
            if is_owner and owner_confirmed:
                return None, "You have already confirmed pickup"
            if is_buyer and user_confirmed:
                return None, "You have already confirmed pickup"

            # Confirm pickup
            result = PurchasesRepository.confirm_pickup(purchase_id, is_owner, is_buyer)

            if not result:
                return None, "Failed to confirm pickup"

            logger.info(
                f"Pickup confirmed for purchase {purchase_id} by "
                f"{'owner' if is_owner else 'buyer'} {confirmer_user_id}"
            )

            return result, None

        except Exception as e:
            logger.error(f"Error in confirm_pickup: {str(e)}")
            return None, f"Error: {str(e)}"

    @staticmethod
    def process_transfer_decision_service(
        purchase_id: str, transfer_ownership: bool, buyer_user_id: str
    ) -> tuple[dict | None, str | None]:
        """
        Processes the buyer's final decision on book ownership transfer.
        If transfer_ownership is true, updates book's owner_id.
        If false, soft-deletes the book.
        In both cases, sets transfer_decision_pending to false.
        """
        try:
            # 1. Verify the purchase exists and the user is the buyer
            # Use get_purchase_with_book_details which includes transfer_decision_pending
            purchase = PurchasesRepository.get_purchase_with_book_details(purchase_id)
            if not purchase:
                return None, "Purchase not found."

            if str(purchase["user_id"]) != str(buyer_user_id):
                return None, "Unauthorized to make this transfer decision."

            # 2. Check current status - the query should return transfer_decision_pending
            if not purchase.get("transfer_decision_pending", False):
                return (
                    None,
                    "Transfer decision is not currently pending for this purchase.",
                )

            # 3. Process the decision in the database
            result = PurchasesRepository.process_transfer_decision(
                purchase_id, transfer_ownership
            )

            if not result:
                return None, "Failed to process transfer decision in the database."

            logger.info(
                f"Transfer decision processed for purchase {purchase_id}. "
                f"Transfer ownership: {transfer_ownership}. "
                f"Buyer: {buyer_user_id}"
            )

            return {
                "purchase_id": purchase_id,
                "transfer_ownership": transfer_ownership,
                "message": "Transfer decision processed successfully.",
            }, None

        except Exception as e:
            logger.error(f"Error in process_transfer_decision_service: {str(e)}")
            traceback.print_exc()
            return None, f"An unexpected error occurred: {str(e)}"
