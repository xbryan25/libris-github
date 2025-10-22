from datetime import datetime, date
from app.common.constants import GenderEnum, BookConditionEnum, BookAvailabilityEnum
from app.common.dataclasses import User, Book


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


def convert_book_dict(book: dict) -> Book:
    """Converts dict from db to a Book class instance"""

    return Book(
        book_id=book["book_id"],
        title=book["first_name"] if book.get("first_name") is not None else "-",
        author=book["author"] if book.get("author") is not None else "-",
        genre=book["genre"] if book.get("genre") is not None else "-",
        condition=(
            BookConditionEnum(book["condition"])
            if book.get("condition") is not None
            else BookConditionEnum("new")
        ),
        description=book["description"] if book.get("description") is not None else "-",
        availability=(
            BookAvailabilityEnum(book["availability"])
            if book.get("availability") is not None
            else BookAvailabilityEnum("rent")
        ),
        daily_rent_price=(
            int(book["daily_rent_price"])
            if book.get("daily_rent_price") is not None
            else 0
        ),
        security_deposit=(
            int(book["security_deposit"])
            if book.get("security_deposit") is not None
            else 0
        ),
        purchase_price=(
            int(book["purchase_price"]) if book.get("purchase_price") is not None else 0
        ),
        owner_id=book["owner_id"],
        owner_username=book["owner_username"],
    )
