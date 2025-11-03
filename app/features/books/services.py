from .repository import BookRepository

from app.common.dataclasses import Book, MyLibraryBook

from app.utils.converters import convert_book_dict, convert_my_library_book_dict

from typing import Any, Optional

from app.utils.date_utils import DateUtils


class BookServices:

    @staticmethod
    def get_books_for_book_list_service(
        params, get_books_from_a_specific_user
    ) -> list[Book]:
        """
        Retrieve details of different books based on pagination, optional search, genre, and availability filters.

        Args:
            params (dict): A dictionary containing the pagination details, optional search, genre, and availability filters.
                Expected keys include:
                    - "books_per_page" (str): The number of book details to retrieve.
                    - "page_number" (str): This number will be multiplied by books_per_page then serve as the
                                            offset for pagination.
                    - "search_value" (str): The value to search for.
                    - "genre" (str): The genre or category of books to filter by.
                    - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".
                    - "user_id" (str): user_id of the user to prevent getting books that the current user owns, or, if from
                                        other user, get all books that that user owns
            get_books_from_a_specific_user (bool): A boolean value that determine whether the books retrived will be from everyone
                                                        or only from a specific user

        Returns:
            list[Book]: A list of Book dataclass instances representing books_per_page books.
        """

        # Clean 'availability' values from 'for rent' to 'rent' and 'for sale' to 'purchase'
        if params["availability"] == "for rent":
            params["availability"] = "rent"
        elif params["availability"] == "for sale":
            params["availability"] = "purchase"

        books = BookRepository.get_books_for_book_list(
            params, get_books_from_a_specific_user
        )

        book_dataclasses = []

        for book in books:
            # Convert dict to dataclass before appending
            book_dataclasses.append(convert_book_dict(book))

        return book_dataclasses

    @staticmethod
    def get_total_book_count_service(
        params, get_book_count_from_a_specific_user
    ) -> int:
        """
        Retrieve the total count of books based on pagination, optional search, genre, and availability filters.

        Args:
            params (dict): A dictionary containing the optional search, genre, and availability filters.
                Expected keys include:
                    - "search_value" (str): The value to search for.
                    - "genre" (str): The genre or category of books to filter by.
                    - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".
                    - "user_id" (str): user_id of the user to prevent counting books that the current user owns, or, if from
                                        other user, count all books that that user owns
            get_book_count_from_a_specific_user (bool): A boolean value that determine whether the books counted will be
                                                        from everyoneor only from a specific user

        Returns:
            int: The total book count, with search, genre, and availability filters being optionally applied.
        """

        # Clean 'availability' values from 'for rent' to 'rent' and 'for sale' to 'purchase'
        if params["availability"] == "for rent":
            params["availability"] = "rent"
        elif params["availability"] == "for sale":
            params["availability"] = "purchase"

        return BookRepository.get_total_book_count(
            params, get_book_count_from_a_specific_user
        )["count"]

    @staticmethod
    def get_my_library_books_service(user_id, params) -> list[MyLibraryBook]:
        """
        Retrieve details of different books based on pagination, optional search, genre, and availability filters.

        Args:
            params (dict): A dictionary containing the pagination details, optional search, genre, and availability filters.
                Expected keys include:
                    - "books_per_page" (str): The number of book details to retrieve.
                    - "page_number" (str): This number will be multiplied by books_per_page then serve as the
                                            offset for pagination.
                    - "search_value" (str): The value to search for.
                    - "genre" (str): The genre or category of books to filter by.
                    - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".
                    - "user_id" (str): user_id of the user to prevent getting books that the current user owns, or, if from
                                        other user, get all books that that user owns
            get_books_from_a_specific_user (bool): A boolean value that determine whether the books retrived will be from everyone
                                                        or only from a specific user

        Returns:
            list[MyLibraryBook]: A list of MyLibraryBook dataclass instances representing books_per_page books.
        """

        # Clean 'availability' values from 'for rent' to 'rent' and 'for sale' to 'purchase'
        if params["availability"] == "for rent":
            params["availability"] = "rent"
        elif params["availability"] == "for sale":
            params["availability"] = "purchase"

        my_library_books = BookRepository.get_my_library_books(user_id, params)

        my_library_book_dataclasses = []

        for my_library_book in my_library_books:
            # Convert dict to dataclass before appending
            my_library_book_dataclasses.append(
                convert_my_library_book_dict(my_library_book)
            )

        # print(my_library_book_dataclasses)
        return my_library_book_dataclasses

    @staticmethod
    def get_total_my_library_book_count_service(user_id, params) -> int:
        """
        Retrieve the total count of books based on pagination, optional search, genre, and availability filters.

        Args:
            params (dict): A dictionary containing the optional search, genre, and availability filters.
                Expected keys include:
                    - "search_value" (str): The value to search for.
                    - "genre" (str): The genre or category of books to filter by.
                    - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".
                    - "user_id" (str): user_id of the user to prevent counting books that the current user owns, or, if from
                                        other user, count all books that that user owns
            get_book_count_from_a_specific_user (bool): A boolean value that determine whether the books counted will be
                                                        from everyoneor only from a specific user

        Returns:
            int: The total book count, with search, genre, and availability filters being optionally applied.
        """

        # Clean 'availability' values from 'for rent' to 'rent' and 'for sale' to 'purchase'
        if params["availability"] == "for rent":
            params["availability"] = "rent"
        elif params["availability"] == "for sale":
            params["availability"] = "purchase"

        return BookRepository.get_total_my_library_book_count(user_id, params)["count"]

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
            "genres": book["genres"],
            "condition": book["condition"],
            "description": book["description"],
            "availability": book["availability"],
            "daily_rent_price": (
                int(book["daily_rent_price"]) if book["daily_rent_price"] else 0
            ),
            "security_deposit": (
                int(book["security_deposit"]) if book["security_deposit"] else 0
            ),
            "purchase_price": (
                int(book["purchase_price"]) if book["purchase_price"] else 0
            ),
            "owner_user_id": book["owner_user_id"],
            "owner_username": book["owner_username"],
            "owner_profile_picture": book["owner_profile_picture"],
            "owner_trust_score": book["owner_trust_score"],
            "times_rented": int(book["times_rented"]),
            "images": [img["image_url"] for img in images],
        }
