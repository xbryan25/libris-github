from dataclasses import dataclass

from app.common.constants import BookAvailabilityEnum, BookConditionEnum


@dataclass
class MyLibraryBook:
    book_id: str
    title: str
    author: str
    genre: str
    condition: BookConditionEnum
    description: str
    availability: BookAvailabilityEnum
    daily_rent_price: int
    security_deposit: int
    purchase_price: int
    rent_status: str | None
    renter_id: str | None
    renter_username: str | None
    renter_profile_image_url: str | None
    first_image_url: str
