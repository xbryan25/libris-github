from flask import current_app
from app.db.queries import DashboardQueries


class DashboardRepository:

    @staticmethod
    def get_summary(user_id: str) -> dict[str, int]:
        """
        Retrieve counts and total earnings for the dashboard, specific to a user.

        Args:
            user_id (str): The ID of the logged-in user.

        Returns:
            dict: A dictionary with keys:
                books_borrowed, currently_lending, currently_renting,
                books_sold, books_bought, total_earnings
        """
        db = current_app.extensions["db"]

        params = tuple([user_id] * 11)

        result = db.fetch_one(DashboardQueries.DASHBOARD_COUNTS, params)

        if result:
            return {
                "books_borrowed": result["books_borrowed"],
                "currently_lending": result["currently_lending"],
                "currently_renting": result["currently_renting"],
                "books_sold": result["books_sold"],
                "books_bought": result["books_bought"],
                "total_earnings": result["total_earnings"],
            }

        return {
            "books_borrowed": 0,
            "currently_lending": 0,
            "currently_renting": 0,
            "books_sold": 0,
            "books_bought": 0,
            "total_earnings": 0,
        }
