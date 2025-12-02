from app.db.queries.purchase_queries import PurchasesQueries
from flask import current_app
from typing import Any
import logging

logger = logging.getLogger(__name__)


class PurchasesRepository:

    @staticmethod
    def insert_purchase(purchase_data: dict) -> dict | None:
        """
        Insert a new purchase record into the database with proper defaults.

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
            dict: The inserted purchase record with purchase_id if successful, None otherwise.
        """
        db = current_app.extensions["db"]

        params = (
            purchase_data["user_id"],
            purchase_data["book_id"],
            purchase_data["reserved_at"],
            purchase_data["reservation_expires_at"],
            purchase_data["total_buy_cost"],
            purchase_data["meetup_time_window"],
            purchase_data["meetup_location"],
            purchase_data["meetup_date"],
        )

        result = db.fetch_one(PurchasesQueries.INSERT_PURCHASE, params)

        if result:
            purchase_data["purchase_id"] = result["purchase_id"]
            return purchase_data

        return None

    @staticmethod
    def exists_pending_purchase(user_id: str, book_id: str) -> bool:
        """
        Check if a pending purchase exists for the given user and book.

        Returns:
            bool: True if a pending purchase exists, False otherwise.
        """
        db = current_app.extensions["db"]
        result = db.fetch_one(
            PurchasesQueries.CHECK_PENDING_PURCHASE, (user_id, book_id)
        )
        return bool(result)

    @staticmethod
    def get_user_purchases_with_status(user_id: str) -> list[dict[str, Any]]:
        """
        Retrieve all purchases for a user with statuses.

        Args:
            user_id (str): The ID of the user whose purchases are being fetched.

        Returns:
            list[dict[str, Any]]: A list of purchase dictionaries with book and owner details.
                Returns empty list if no purchases found.
        """
        db = current_app.extensions["db"]
        params = (user_id,)

        result = db.fetch_all(PurchasesQueries.GET_USER_PURCHASES_WITH_STATUS, params)
        return result if result else []

    @staticmethod
    def get_user_sales_with_status(user_id: str) -> list[dict[str, Any]]:
        """
        Retrieve all sales for a user with statuses.

        Args:
            user_id (str): The ID of the user whose sales are being fetched.

        Returns:
            list[dict[str, Any]]: A list of sale dictionaries with book and buyer details.
                Returns empty list if no sales found.
        """
        db = current_app.extensions["db"]
        params = (user_id,)

        result = db.fetch_all(PurchasesQueries.GET_USER_SALES_WITH_STATUS, params)
        return result if result else []

    @staticmethod
    def get_purchase_by_id(purchase_id: str) -> dict[str, Any] | None:
        """
        Retrieve purchase details by purchase ID.
        """
        db = current_app.extensions["db"]
        params = (purchase_id,)
        result = db.fetch_one(PurchasesQueries.GET_PURCHASE_BY_ID, params)
        return result

    @staticmethod
    def approve_purchase(purchase_id: str, meetup_time: str) -> dict[str, Any] | None:
        """
        Approve a purchase and set meetup time.

        Args:
            purchase_id (str): The purchase ID to approve.
            meetup_time (str): The meetup time (HH:MM format).

        Returns:
            dict[str, Any] | None: Updated purchase details or None if update failed.
        """
        db = current_app.extensions["db"]
        params = (meetup_time, purchase_id)

        result = db.fetch_one(PurchasesQueries.APPROVE_PURCHASE, params)

        return result

    @staticmethod
    def delete_purchase(purchase_id: str) -> dict[str, Any] | None:
        """
        Delete a purchase entry from purchased_books.

        Args:
            purchase_id (str): The purchase ID to delete.

        Returns:
            dict[str, Any] | None: Deleted purchase ID or None if deletion failed.
        """
        db = current_app.extensions["db"]
        params = (purchase_id,)

        result = db.fetch_one(PurchasesQueries.DELETE_PURCHASE, params)

        return result

    @staticmethod
    def get_purchase_by_id_full(purchase_id: str) -> dict[str, Any] | None:
        """
        Retrieve full purchase details by purchase ID including confirmation statuses.
        """
        db = current_app.extensions["db"]
        params = (purchase_id,)
        result = db.fetch_one(PurchasesQueries.GET_PURCHASE_BY_ID_FULL, params)
        return result

    @staticmethod
    def confirm_pickup(
        purchase_id: str, is_owner: bool, is_buyer: bool
    ) -> dict[str, Any] | None:
        """
        Confirm pickup by owner or buyer.
        If both have confirmed, update status to 'completed'.
        """
        db = current_app.extensions["db"]

        params = (
            is_owner,
            is_buyer,
            is_owner,
            is_buyer,
            purchase_id,
        )

        result = db.fetch_one(PurchasesQueries.CONFIRM_PICKUP, params)
        return result

    @staticmethod
    def check_book_availability(book_id: str, owner_id: str) -> dict[str, Any] | None:
        """
        Check if a book already has an active purchase (approved or awaiting pickup).

        Args:
            book_id (str): The book ID to check
            owner_id (str): The owner ID to verify ownership

        Returns:
            dict with purchase details if book is unavailable, None if available
        """
        db = current_app.extensions["db"]
        params = (book_id, owner_id)
        result = db.fetch_one(PurchasesQueries.CHECK_BOOK_AVAILABILITY, params)
        return result

    @staticmethod
    def get_book_id_from_purchase(purchase_id: str) -> str | None:
        """
        Get the book_id for a given purchase.

        Args:
            purchase_id (str): The purchase ID

        Returns:
            str: The book_id or None if not found
        """
        db = current_app.extensions["db"]
        result = db.fetch_one(
            PurchasesQueries.GET_BOOK_ID_FROM_PURCHASE, (purchase_id,)
        )
        return result.get("book_id") if result else None
