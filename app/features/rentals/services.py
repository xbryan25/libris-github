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
                    DateUtils.extract_date(rental.get("meetup_date"))
                    if rental.get("meetup_date")
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

    @staticmethod
    def get_user_lendings_with_status(user_id: str) -> list[dict[str, Any]]:
        raw_lendings = RentalRepository.get_user_lendings_with_status(user_id)

        formatted_lendings = []
        for lending in raw_lendings:
            formatted_lending = {
                "rental_id": lending.get("rental_id"),
                "rent_status": lending.get("rent_status"),
                "book_id": lending.get("book_id"),
                "title": lending.get("title", ""),
                "author": lending.get("author", ""),
                "image": lending.get("image"),
                "to": lending.get("to", ""),
                "all_fees_captured": lending.get("all_fees_captured", False),
                "reserved_at": lending.get("reserved_at"),
                "reservation_expires_at": lending.get("reservation_expires_at"),
                "rental_duration_days": lending.get("rental_duration_days", 0),
                "meetup_location": lending.get("meetup_location", ""),
                "meetup_time_window": lending.get("meetup_time_window", ""),
                "pickup_confirmation_started_at": lending.get(
                    "pickup_confirmation_started_at"
                ),
                "user_confirmed_pickup": lending.get("user_confirmed_pickup", False),
                "owner_confirmed_pickup": lending.get("owner_confirmed_pickup", False),
                "return_confirmation_started_at": lending.get(
                    "return_confirmation_started_at"
                ),
                "user_confirmed_return": lending.get("user_confirmed_return", False),
                "owner_confirmed_return": lending.get("owner_confirmed_return", False),
                "cost": (
                    int(lending.get("cost", 0))
                    if lending.get("cost") not in (None, "")
                    else 0
                ),
                # Date and time separated
                "meetup_date": (
                    DateUtils.extract_date(lending.get("meetup_date"))
                    if lending.get("meetup_date")
                    else None
                ),
                "meetup_time": (
                    DateUtils.extract_time(lending.get("meetup_time"))
                    if lending.get("meetup_time")
                    else None
                ),
                "rent_start_date": (
                    DateUtils.extract_date(lending.get("rent_start_date"))
                    if lending.get("rent_start_date")
                    else None
                ),
                "rent_end_date": (
                    DateUtils.extract_date(lending.get("rent_end_date"))
                    if lending.get("rent_end_date")
                    else None
                ),
            }
            formatted_lendings.append(formatted_lending)
        return formatted_lendings
