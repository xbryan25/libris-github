from flask import current_app
from app.db.queries.purchase_queries import PurchasedBooksQueries


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

        result = db.fetch_one(PurchasedBooksQueries.INSERT_PURCHASE, params)

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
            PurchasedBooksQueries.CHECK_PENDING_PURCHASE, (user_id, book_id)
        )
        return bool(result)
