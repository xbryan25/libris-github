from app.db.queries import CommonQueries

from flask import current_app


class NotificationRepository:
    @staticmethod
    def get_notifications(user_id, params) -> list[dict[str, str]]:
        """
        add later
        """

        db = current_app.extensions["db"]

        offset = (
            0
            if params["page_number"] <= 0
            else (params["page_number"] - 1) * params["rows_per_page"]
        )

        if params["read_status"] == "show all":
            return db.fetch_all(
                CommonQueries.GET_MANY.format(
                    table="notifications",
                    conditions="receiver_id = %s",
                    sort_field="created_at",
                    sort_order="DESC",
                ),
                (user_id, params["rows_per_page"], offset),
            )

        else:
            if params["read_status"] == "show only read":
                read_status_bool = True
            else:
                read_status_bool = False

            return db.fetch_all(
                CommonQueries.GET_MANY.format(
                    table="notifications",
                    conditions="receiver_id = %s AND is_read = %s",
                    sort_field="created_at",
                    sort_order="DESC",
                ),
                (user_id, read_status_bool, params["rows_per_page"], offset),
            )

    @staticmethod
    def get_notifications_total_count(user_id, params) -> dict[str, int]:
        """
        add later
        """

        db = current_app.extensions["db"]

        if params["read_status"] == "show all":
            return db.fetch_one(
                CommonQueries.GET_TOTAL_COUNT_WITH_CONDITIONS.format(
                    table="notifications", conditions="receiver_id = %s"
                ),
                (user_id,),
            )

        else:
            if params["read_status"] == "show only read":
                read_status_bool = True
            else:
                read_status_bool = False

            return db.fetch_one(
                CommonQueries.GET_TOTAL_COUNT_WITH_CONDITIONS.format(
                    table="notifications",
                    conditions="receiver_id = %s AND is_read = %s",
                ),
                (user_id, read_status_bool),
            )
