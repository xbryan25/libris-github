from flask import current_app
from app.db.queries.rating_queries import RatingQueries
from typing import Optional
from app.db.queries.common import CommonQueries


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
    def get_user_trust_score(user_id: str) -> int:
        """Get a user's current trust score."""
        db = current_app.extensions["db"]
        result = db.fetch_one(
            CommonQueries.GET_COLUMN_BY_FIELD.format(
                column="trust_score", table="users", field="user_id"
            ),
            (user_id,),
        )
        if result:
            return result["trust_score"]
        else:
            raise ValueError(f"User {user_id} not found when attempting to rate.")

    @staticmethod
    def update_user_trust_score(user_id: str, new_score: int) -> None:
        """Update the user's trust score in the users table."""
        db = current_app.extensions["db"]
        db.fetch_one(RatingQueries.UPDATE_USER_TRUST_SCORE, (new_score, user_id))

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

    @staticmethod
    def get_ratings_from_rental_from_rater(
        rental_id: str, rater_id: str
    ) -> dict[str, int | str] | None:
        """Get rating score and comment from rental_id and rater_id"""
        db = current_app.extensions["db"]

        return db.fetch_one(
            RatingQueries.GET_RATINGS_FROM_RENTAL_FROM_RATER, (rental_id, rater_id)
        )

    @staticmethod
    def get_ratings_from_rental_from_rated_user(
        rental_id: str, rated_user_id: str
    ) -> dict[str, int | str] | None:
        """Get rating score and comment from rental_id and rated_user_id"""
        db = current_app.extensions["db"]

        return db.fetch_one(
            RatingQueries.GET_RATINGS_FROM_RENTAL_FROM_RATED_USER,
            (rental_id, rated_user_id),
        )

    @staticmethod
    def get_ratings_from_purchase_from_rater(
        purchase_id: str, rater_id: str
    ) -> dict[str, int | str] | None:
        """Get rating score and comment from purchase_id and rater_id"""
        db = current_app.extensions["db"]

        return db.fetch_one(
            RatingQueries.GET_RATINGS_FROM_PURCHASE_FROM_RATER, (purchase_id, rater_id)
        )

    @staticmethod
    def get_ratings_from_purchase_from_rated_user(
        purchase_id: str, rated_user_id: str
    ) -> dict[str, int | str] | None:
        """Get rating score and comment from purchase_id and rated_user_id"""
        db = current_app.extensions["db"]

        return db.fetch_one(
            RatingQueries.GET_RATINGS_FROM_PURCHASE_FROM_RATED_USER,
            (purchase_id, rated_user_id),
        )
