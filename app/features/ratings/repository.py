from flask import current_app
from app.db.queries.rating_queries import RatingQueries
from typing import Optional


class RatingRepository:

    @staticmethod
    def get_rental_info(rental_id: str) -> dict | None:
        """Get rental information."""
        db = current_app.extensions["db"]
        return db.fetch_one(RatingQueries.GET_RENTAL_INFO, (rental_id,))

    @staticmethod
    def insert_rating(
        rater_id: str,
        rated_user_id: str,
        score: int,
        comment: str,
        rental_id: Optional[str] = None,
        purchase_id: Optional[str] = None,
    ) -> dict | None:
        """Insert a rating into database."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            RatingQueries.INSERT_RATING,
            (rater_id, rated_user_id, score, comment, rental_id, purchase_id),
        )

    @staticmethod
    def update_user_rated_flag(rental_id: str) -> None:
        """Set user_rated to TRUE."""
        db = current_app.extensions["db"]
        db.fetch_one(RatingQueries.UPDATE_USER_RATED_FLAG, (rental_id,))

    @staticmethod
    def update_owner_rated_flag(rental_id: str) -> None:
        """Set owner_rated to TRUE."""
        db = current_app.extensions["db"]
        db.fetch_one(RatingQueries.UPDATE_OWNER_RATED_FLAG, (rental_id,))

    @staticmethod
    def get_purchase_info(purchase_id: str) -> dict | None:
        """Get purchase information."""
        db = current_app.extensions["db"]
        return db.fetch_one(RatingQueries.GET_PURCHASE_INFO, (purchase_id,))

    @staticmethod
    def update_purchase_user_rated_flag(purchase_id: str) -> None:
        """Set user_rated to TRUE for purchase."""
        db = current_app.extensions["db"]
        db.fetch_one(RatingQueries.UPDATE_PURCHASE_USER_RATED_FLAG, (purchase_id,))

    @staticmethod
    def update_purchase_owner_rated_flag(purchase_id: str) -> None:
        """Set owner_rated to TRUE for purchase."""
        db = current_app.extensions["db"]
        db.fetch_one(RatingQueries.UPDATE_PURCHASE_OWNER_RATED_FLAG, (purchase_id,))

    @staticmethod
    def check_existing_purchase_rating(purchase_id: str, rater_id: str) -> bool:
        """Check if a rating already exists for a purchase."""
        db = current_app.extensions["db"]
        result = db.fetch_one(
            RatingQueries.CHECK_EXISTING_RATING_PURCHASE, (purchase_id, rater_id)
        )
        return result.get("exists") if result else False
