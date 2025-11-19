from app.db.queries import CommonQueries

from flask import current_app


class NotificationRepository:
    @staticmethod
    def get_recent_notifications(user_id, num_of_notifications) -> list[dict[str, str]]:
        """
        add later
        """

        db = current_app.extensions["db"]

        return db.fetch_all(
            CommonQueries.GET_MANY.format(
                table="notifications",
                conditions="receiver_id = %s AND is_read = %s",
                sort_field="created_at",
                sort_order="DESC",
            ),
            (user_id, False, num_of_notifications, 0),
        )
