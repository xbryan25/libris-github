from .repository import RentalRepository
from typing import Any
from app.utils import DateUtils


class RentalServices:
    @staticmethod
    def get_user_rentals_with_status(user_id: str) -> list[dict[str, Any]]:
        raw_rentals = RentalRepository.get_user_rentals_with_status(user_id)

        formatted_rentals = []
        for rental in raw_rentals:
            formatted_rental = {
                "rental_id": rental.get("rental_id"),
                "rent_status": rental.get("rent_status"),
                "book_id": rental.get("book_id"),
                "title": rental.get("title", ""),
                "author": rental.get("author", ""),
                "image": rental.get("image"),
                "from": rental.get("from", ""),
                "all_fees_captured": rental.get("all_fees_captured", False),
                "reserved_at": rental.get("reserved_at"),
                "reservation_expires_at": rental.get("reservation_expires_at"),
                "rental_duration_days": rental.get("rental_duration_days", 0),
                "meetup_location": rental.get("meetup_location", ""),
                "meetup_time_window": rental.get("meetup_time_window", ""),
                "pickup_confirmation_started_at": rental.get(
                    "pickup_confirmation_started_at"
                ),
                "user_confirmed_pickup": rental.get("user_confirmed_pickup", False),
                "owner_confirmed_pickup": rental.get("owner_confirmed_pickup", False),
                "return_confirmation_started_at": rental.get(
                    "return_confirmation_started_at"
                ),
                "user_confirmed_return": rental.get("user_confirmed_return", False),
                "owner_confirmed_return": rental.get("owner_confirmed_return", False),
                "cost": (
                    int(rental.get("cost", 0))
                    if rental.get("cost") not in (None, "")
                    else 0
                ),
                # Date and time separated
                "meetup_date": (
                    DateUtils.extract_date(rental.get("meetup_time"))
                    if rental.get("meetup_time")
                    else None
                ),
                "meetup_time": (
                    DateUtils.extract_time(rental.get("meetup_time"))
                    if rental.get("meetup_time")
                    else None
                ),
                "rent_start_date": (
                    DateUtils.extract_date(rental.get("rent_start_date"))
                    if rental.get("rent_start_date")
                    else None
                ),
                "rent_end_date": (
                    DateUtils.extract_date(rental.get("rent_end_date"))
                    if rental.get("rent_end_date")
                    else None
                ),
            }
            formatted_rentals.append(formatted_rental)

        return formatted_rentals
