from .repository import NotificationRepository

from app.common.dataclasses import Notification

from app.utils import convert_notification_dict

from app import socketio


class NotificationServices:

    @staticmethod
    def add_notification_service(
        sender_user_id, receiver_user_id, notification_type, header, message
    ) -> None:
        """
        add later
        """

        NotificationRepository.add_notification(
            sender_user_id, receiver_user_id, notification_type, header, message
        )

        unread_notifications_count = (
            NotificationServices.get_notifications_total_count_service(
                receiver_user_id, {"read_status": "show only unread"}
            )
        )

        socketio.start_background_task(
            NotificationServices._emit_notification,
            receiver_user_id,
            unread_notifications_count,
        )

    @staticmethod
    def _emit_notification(receiver_user_id, count):
        socketio.emit(
            "update_unread_notifications_count",
            {"unreadNotificationsCount": count},
            room=str(receiver_user_id),
        )

    @staticmethod
    def get_notifications_service(user_id, params) -> list[Notification]:
        """
        add later
        """

        # Clean 'order' values from 'show newest first' to 'DESC' and 'show oldest first' to 'ASC'
        if params["order"] == "show newest first":
            params["order"] = "DESC"
        elif params["order"] == "show oldest first":
            params["order"] = "ASC"
        else:
            params["order"] = "DESC"

        notifications = NotificationRepository.get_notifications(user_id, params)

        notification_dataclasses = []

        for notification in notifications:
            # Convert dict to dataclass before appending
            notification_dataclasses.append(convert_notification_dict(notification))

        return notification_dataclasses

    @staticmethod
    def get_notifications_total_count_service(user_id, params) -> int:
        """
        add later
        """

        return NotificationRepository.get_notifications_total_count(user_id, params)[
            "count"
        ]

    @staticmethod
    def mark_notification_as_read_service(notification_id: str) -> None:
        """
        add later
        """

        NotificationRepository.mark_notification_as_read(notification_id)

    @staticmethod
    def change_notifications_read_status_service(
        notification_ids: list[str], is_read_change: bool
    ) -> None:
        """
        add later
        """

        NotificationRepository.change_notifications_read_status(
            notification_ids, is_read_change
        )

    @staticmethod
    def delete_notifications_service(notification_ids: list[str]) -> None:
        """
        add later
        """

        NotificationRepository.delete_notifications(notification_ids)
