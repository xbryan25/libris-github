from dataclasses import dataclass

from app.common.constants import BookAvailabilityEnum, BookConditionEnum


@dataclass
class Book:
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
    owner_id: str
    owner_username: str
    first_image_url: str
