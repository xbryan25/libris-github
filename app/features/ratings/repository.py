from flask import current_app
from app.db.queries.rating_queries import RatingQueries
from app.db.queries.common import CommonQueries


class RatingRepository:

    @staticmethod
    def get_rental_info(rental_id: str) -> dict | None:
        """Get rental information."""
        db = current_app.extensions["db"]
        return db.fetch_one(RatingQueries.GET_RENTAL_INFO, (rental_id,))

    @staticmethod
    def insert_rating(
        rater_id: str, rated_user_id: str, score: int, comment: str
    ) -> dict | None:
        """Insert a rating into database."""
        db = current_app.extensions["db"]
        return db.fetch_one(
            RatingQueries.INSERT_RATING, (rater_id, rated_user_id, score, comment)
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
