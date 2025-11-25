from datetime import datetime, date
from app.common.constants import (
    GenderEnum,
    BookConditionEnum,
    BookAvailabilityEnum,
    NotificationTypeEnum,
    AuthProviderEnum,
)

from app.common.dataclasses import User, Book, MyLibraryBook, Notification


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
        auth_provider=AuthProviderEnum(user["auth_provider"]),
        is_email_verified=user["is_email_verified"],
    )


def convert_book_dict(book: dict) -> Book:
    """Converts dict from db to a Book class instance"""

    return Book(
        book_id=book["book_id"],
        title=book["title"] if book.get("title") is not None else "-",
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
        first_image_url=book["first_image_url"],
    )


def convert_my_library_book_dict(my_library_book: dict) -> MyLibraryBook:
    """Converts dict from db to a Book class instance"""

    return MyLibraryBook(
        book_id=my_library_book["book_id"],
        title=(
            my_library_book["title"]
            if my_library_book.get("title") is not None
            else "-"
        ),
        author=(
            my_library_book["author"]
            if my_library_book.get("author") is not None
            else "-"
        ),
        genre=(
            my_library_book["genre"]
            if my_library_book.get("genre") is not None
            else "-"
        ),
        condition=(
            BookConditionEnum(my_library_book["condition"])
            if my_library_book.get("condition") is not None
            else BookConditionEnum("new")
        ),
        description=(
            my_library_book["description"]
            if my_library_book.get("description") is not None
            else "-"
        ),
        availability=(
            BookAvailabilityEnum(my_library_book["availability"])
            if my_library_book.get("availability") is not None
            else BookAvailabilityEnum("rent")
        ),
        daily_rent_price=(
            int(my_library_book["daily_rent_price"])
            if my_library_book.get("daily_rent_price") is not None
            else 0
        ),
        security_deposit=(
            int(my_library_book["security_deposit"])
            if my_library_book.get("security_deposit") is not None
            else 0
        ),
        purchase_price=(
            int(my_library_book["purchase_price"])
            if my_library_book.get("purchase_price") is not None
            else 0
        ),
        rent_status=my_library_book["rent_status"],
        renter_id=my_library_book["renter_id"],
        renter_username=my_library_book["renter_username"],
        renter_profile_image_url=my_library_book["renter_profile_image_url"],
        first_image_url=my_library_book["first_image_url"],
    )


def convert_notification_dict(notification: dict) -> Notification:
    """Converts dict from db to a Book class instance"""

    return Notification(
        notification_id=notification["notification_id"],
        header=(
            notification["header"] if notification.get("header") is not None else "-"
        ),
        message=(
            notification["message"] if notification.get("message") is not None else "-"
        ),
        created_at=(
            notification["created_at"]
            if isinstance(notification.get("created_at"), datetime)
            or notification.get("created_at") is None
            else datetime.fromisoformat(notification["created_at"])
        ),
        is_read=(
            notification["is_read"]
            if notification.get("is_read") is not None
            else False
        ),
        notification_type=(
            NotificationTypeEnum(notification["notification_type"])
            if notification.get("notification_type") is not None
            else NotificationTypeEnum("rent")
        ),
        sender_id=notification["sender_id"],
        receiver_id=notification["receiver_id"],
    )
