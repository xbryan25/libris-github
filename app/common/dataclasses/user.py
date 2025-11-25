from dataclasses import dataclass
from datetime import date, datetime
from werkzeug.security import check_password_hash

from app.common.constants import GenderEnum, AuthProviderEnum


@dataclass
class User:
    user_id: str
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    date_of_birth: date | None
    gender: GenderEnum | None
    phone_number: str | None
    email_address: str
    account_activated_at: datetime | None
    username: str
    password_hash: str
    trust_score: int
    profile_completed: datetime | None
    profile_image_url: str | None
    auth_provider: AuthProviderEnum
    is_email_verified: bool

    def check_password(self, password: str) -> bool:
        """Validate plaintext password against the hashed one."""
        return check_password_hash(self.password_hash, password)
