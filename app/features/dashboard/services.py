from .repository import DashboardRepository


class DashboardServices:

    @staticmethod
    def get_user_dashboard(user_id: str) -> dict[str, int]:
        """
        Fetch the dashboard statistics for a specific user.

        Args:
            user_id (str): The ID of the logged-in user.

        Returns:
            dict: Dictionary containing dashboard metrics:
                books_borrowed, currently_lending, currently_renting,
                books_sold, books_bought, total_earnings
        """
        return DashboardRepository.get_summary(user_id)
