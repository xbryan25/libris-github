from .repository import NotificationRepository

from app.common.dataclasses import Notification

from app.utils import convert_notification_dict


class NotificationServices:
    @staticmethod
    def get_recent_notifications_service(
        user_id, num_of_notifications
    ) -> list[Notification]:
        """
        add later
        """

        notifications = NotificationRepository.get_recent_notifications(
            user_id, num_of_notifications
        )

        print(notifications)

        notification_dataclasses = []

        for notification in notifications:
            # Convert dict to dataclass before appending
            notification_dataclasses.append(convert_notification_dict(notification))

        return notification_dataclasses
