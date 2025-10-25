from .repository import BookRepository

from app.common.dataclasses import Book

from app.utils.converters import convert_book_dict

from typing import Any, Optional

from app.utils.date_utils import DateUtils


class BookServices:

    @staticmethod
    def get_many_books_service(user_id, params) -> list[Book]:
        """
        Retrieve details of different books based on pagination, optional search, genre, and availability filters.

        Args:
            user_id (str): user_id of the user to prevent getting books that the current user owns.
            params (dict): A dictionary containing the pagination details, optional search, genre, and availability filters.
                Expected keys include:
                    - "books_per_page" (str): The number of book details to retrieve.
                    - "page_number" (str): This number will be multiplied by books_per_page then serve as the
                                            offset for pagination.
                    - "search_value" (str): The value to search for.
                    - "genre" (str): The genre or category of books to filter by.
                    - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".

        Returns:
            list[Book]: A list of Book dataclass instances representing books_per_page students.
        """

        # Clean 'availability' values from 'for rent' to 'rent' and 'for sale' to 'purchase'
        if params["availability"] == "for rent":
            params["availability"] = "rent"
        elif params["availability"] == "for sale":
            params["availability"] = "purchase"

        books = BookRepository.get_many_books(user_id, params)

        book_dataclasses = []

        for book in books:
            # Convert dict to dataclass before appending
            book_dataclasses.append(convert_book_dict(book))

        return book_dataclasses

    @staticmethod
    def get_total_book_count_service(user_id, params) -> int:
        """
        Retrieve the total count of books based on pagination, optional search, genre, and availability filters.

        Args:
            params (dict): A dictionary containing the optional search, genre, and availability filters.
                Expected keys include:
                    - "search_value" (str): The value to search for.
                    - "genre" (str): The genre or category of books to filter by.
                    - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".

        Returns:
            int: The total book count, with search, genre, and availability filters being optionally applied.
        """

        # Clean 'availability' values from 'for rent' to 'rent' and 'for sale' to 'purchase'
        if params["availability"] == "for rent":
            params["availability"] = "rent"
        elif params["availability"] == "for sale":
            params["availability"] = "purchase"

        return BookRepository.get_total_book_count(user_id, params)["count"]

    @staticmethod
    def get_book_genres_service() -> list[str]:
        """
        Retrieve a list of available genres.

        Returns:
            [str]: A list containing all available book genres.
        """

        dict_book_genres: list[dict[str, str]] = BookRepository.get_book_genres()

        book_genres = [
            dict_book_genre["book_genre_name"] for dict_book_genre in dict_book_genres
        ]

        return book_genres

    @staticmethod
    def get_renting_books_service(user_id: str) -> list[dict[str, Any]]:
        """Get books currently being rented by user"""
        books = BookRepository.get_renting_books(user_id)

        formatted_books = []
        for book in books:
            formatted_book = dict(book)
            formatted_book["returnDate"] = DateUtils.format_date(book["return_date"])
            formatted_book["cost"] = str(book["cost"])
            formatted_books.append(formatted_book)

        return formatted_books

    @staticmethod
    def get_bought_books_service(user_id: str) -> list[dict[str, Any]]:
        """Get books purchased by user"""
        books = BookRepository.get_bought_books(user_id)

        formatted_books = []
        for book in books:
            formatted_book = dict(book)
            formatted_book["cost"] = str(book["cost"])
            formatted_books.append(formatted_book)

        return formatted_books

    @staticmethod
    def get_lent_books_service(user_id: str) -> list[dict[str, Any]]:
        """Get books owned by user that are rented by others"""
        books = BookRepository.get_lent_books(user_id)

        formatted_books = []
        for book in books:
            formatted_book = dict(book)
            formatted_book["returnDate"] = DateUtils.format_date(book["return_date"])
            formatted_book["cost"] = str(book["cost"])
            formatted_books.append(formatted_book)

        return formatted_books

    @staticmethod
    def get_sold_books_service(user_id: str) -> list[dict[str, Any]]:
        """Get books owned by user that were purchased by others"""
        books = BookRepository.get_sold_books(user_id)

        formatted_books = []
        for book in books:
            formatted_book = dict(book)
            formatted_book["cost"] = str(book["cost"])
            formatted_books.append(formatted_book)

        return formatted_books

    @staticmethod
    def get_all_user_books_service(user_id: str) -> dict[str, list[dict[str, Any]]]:
        """Get all books data for a user in the required format"""
        return {
            "renting": BookServices.get_renting_books_service(user_id),
            "bought": BookServices.get_bought_books_service(user_id),
            "rented-by-others": BookServices.get_lent_books_service(user_id),
            "bought-by-others": BookServices.get_sold_books_service(user_id),
        }

    @staticmethod
    def get_book_details_service(book_id: str) -> Optional[dict[str, Any]]:
        """Get detailed information about a specific book"""
        book = BookRepository.get_book_details(book_id)

        if not book:
            return None

        images = BookRepository.get_book_images(book_id)

        return {
            "book_id": book["book_id"],
            "title": book["title"],
            "author": book["author"],
            "genre": book["genre"],
            "condition": book["condition"],
            "description": book["description"],
            "availability": book["availability"],
            "daily_rent_price": book["daily_rent_price"],
            "security_deposit": book["security_deposit"],
            "purchase_price": book["purchase_price"],
            "owner_username": book["owner_username"],
            "owner_trust_score": book["owner_trust_score"],
            "images": [img["image_url"] for img in images],
        }
