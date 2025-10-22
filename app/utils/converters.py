from datetime import datetime, date
from app.common.constants import GenderEnum
from app.common.dataclasses import User


def convert_user_dict(user: dict) -> User:
    """Converts dict from db to a User class instance"""

    return User(
        user_id=user["user_id"],
        first_name=user.get("first_name"),
        middle_name=user.get("middle_name"),
        last_name=user.get("last_name"),
        date_of_birth=(
            user["date_of_birth"]
            if isinstance(user.get("date_of_birth"), date)
            or user.get("date_of_birth") is None
            else date.fromisoformat(user["date_of_birth"])
        ),
        gender=GenderEnum(user["gender"]) if user.get("gender") is not None else None,
        phone_number=user.get("phone_number"),
        email_address=user["email_address"],
        account_activated_at=(
            user["account_activated_at"]
            if isinstance(user.get("account_activated_at"), datetime)
            or user.get("account_activated_at") is None
            else datetime.fromisoformat(user["account_activated_at"])
        ),
        username=user["username"],
        password_hash=user["password_hash"],
        trust_score=(
            int(user["trust_score"]) if user.get("trust_score") is not None else 0
        ),
        profile_completed=(
            user["profile_completed"]
            if isinstance(user.get("profile_completed"), datetime)
            or user.get("profile_completed") is None
            else datetime.fromisoformat(user["profile_completed"])
        ),
        profile_image_url=user.get("profile_image_url"),
    )
