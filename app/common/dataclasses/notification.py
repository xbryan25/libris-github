from dataclasses import dataclass
from datetime import datetime

from app.common.constants import NotificationTypeEnum


@dataclass
class Notification:
    notification_id: str
    header: str
    message: str
    created_at: datetime | None
    is_read: bool
    notification_type: NotificationTypeEnum
    sender_id: str | None
    receiver_id: str
