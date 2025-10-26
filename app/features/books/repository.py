from typing import Any, Optional
from flask import current_app
from app.db.queries.book_queries import BookQueries


class BookRepository:
    @staticmethod
    def get_book_details(book_id: str) -> Optional[dict[str, Any]]:
        """
        Retrieve detailed information about a specific book.

        Args:
            book_id (str): The unique identifier of the book.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing book details. The dictionary includes:
                - book_id (str): Book ID
                - title (str): Title of the book
                - author (str): Author of the book
                - genre (str): Genre of the book
                - condition (str): Book condition (e.g., 'new', 'used')
                - description (str): Description of the book
                - availability (str): Current availability status
                - daily_rent_price (int): Daily rental price
                - security_deposit (int): Required security deposit
                - purchase_price (int): Price if the book is for sale
                - owner_username (str): Username of the book's owner
                - owner_trust_score (int): Trust score of the owner
        """
        db = current_app.extensions["db"]

        params = tuple([book_id] * 11)

        return db.fetch_one(BookQueries.BOOK_DETAILS, params)

    @staticmethod
    def get_book_images(book_id: str) -> list[dict[str, Any]]:
        """
        Retrieve all images associated with a specific book, ordered by their display order.

        Args:
            book_id (str): The unique identifier of the book.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing:
                - image_url (str): The URL of the book image
                - order_num (int): The display order of the image
        """
        db = current_app.extensions["db"]

        params = tuple([book_id] * 11)

        return db.fetch_all(BookQueries.BOOK_IMAGES, params)

    @staticmethod
    def get_renting_books(user_id: str) -> list[dict[str, Any]]:
        """
        Retrieve books currently being rented by the specified user.

        Args:
            user_id (str): The ID of the user whose rented books are being fetched.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a rented book
            with details such as:
                - id (str): Book ID
                - title (str): Book title
                - author (str): Book author
                - image (str | None): URL of the book's primary image
                - from (str): Username of the book owner
                - return_date (datetime): Due date for return
                - cost (int): Total rent cost
        """

        db = current_app.extensions["db"]

        params = (user_id,)

        return db.fetch_all(BookQueries.RENTED_BOOKS, params)

    @staticmethod
    def get_bought_books(user_id: str) -> list[dict[str, Any]]:
        """
        Retrieve books purchased by the specified user.

        Args:
            user_id (str): The ID of the user whose purchased books are being fetched.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a purchased book
            with details such as:
                - id (str): Book ID
                - title (str): Book title
                - author (str): Book author
                - image (str | None): URL of the book's primary image
                - from (str): Username of the seller
                - cost (int): Total purchase cost
        """

        db = current_app.extensions["db"]

        params = (user_id,)

        return db.fetch_all(BookQueries.BOUGHT_BOOKS, params)

    @staticmethod
    def get_lent_books(user_id: str) -> list[dict[str, Any]]:
        """
        Retrieve books owned by the specified user that are lent to others.

        Args:
            user_id (str): The ID of the user (book owner).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a rented-out book
            with details such as:
                - id (str): Book ID
                - title (str): Book title
                - author (str): Book author
                - image (str | None): URL of the book's primary image
                - by (str): Username of the renter
                - return_date (datetime): Due date for return
                - cost (int): Total rent cost
        """

        db = current_app.extensions["db"]

        params = (user_id,)

        return db.fetch_all(BookQueries.LENT_BOOKS, params)

    @staticmethod
    def get_sold_books(user_id: str) -> list[dict[str, Any]]:
        """
        Retrieve books owned by the specified user that have been purchased by others.

        Args:
        user_id (str): The ID of the user (book owner).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a sold book
            with details such as:
                - id (str): Book ID
                - title (str): Book title
                - author (str): Book author
                - image (str | None): URL of the book's primary image
                - by (str): Username of the buyer
                - cost (int): Total sale amount
        """

        db = current_app.extensions["db"]

        params = (user_id,)

        return db.fetch_all(BookQueries.SOLD_BOOKS, params)
