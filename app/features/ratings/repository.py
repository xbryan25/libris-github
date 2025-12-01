from flask import current_app
from app.db.queries.rating_queries import RatingQueries


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
    def update_user_rated_flag(rental_id: str) -> None:
        """Set user_rated to TRUE."""
        db = current_app.extensions["db"]
        db.fetch_one(RatingQueries.UPDATE_USER_RATED_FLAG, (rental_id,))

    @staticmethod
    def update_owner_rated_flag(rental_id: str) -> None:
        """Set owner_rated to TRUE."""
        db = current_app.extensions["db"]
        db.fetch_one(RatingQueries.UPDATE_OWNER_RATED_FLAG, (rental_id,))
