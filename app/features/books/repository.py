from app.db.queries import BookQueries, CommonQueries

from flask import current_app
from typing import Any, Optional


class BookRepository:
    @staticmethod
    def get_books_for_book_list(user_id, params) -> list[dict[str, str]]:
        """
        Retrieve a paginated list of books based on search, genre, and availability filters.

        Args:
            user_id (str): user_id of the user to prevent getting books that the current user owns.
            params (dict): A dictionary of query parameters. Expected keys include:
                - "books_per_page" (str): The number of book details to retrieve.
                - "page_number" (str): This number will be multiplied by books_per_page then serve as the offset for pagination.
                - "search_value" (str): The value to search for.
                - "genre" (str): The genre or category of books to filter by.
                - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".

        Returns:
            list[dict]: A list of book records matching the given filters, where each record is represented as a dictionary.
        """

        db = current_app.extensions["db"]

        offset = (
            0
            if params["page_number"] <= 0
            else (params["page_number"] - 1) * params["books_per_page"]
        )

        # Search is 'Contains'
        search_pattern = f"%{params['search_value']}%"

        genre = "%%" if params["genre"] == "all genres" else f"{params['genre']}"
        availability = (
            "%%" if params["availability"] == "all" else f"{params['availability']}"
        )

        # Randomized
        return db.fetch_all(
            BookQueries.GET_BOOKS_FOR_BOOK_LIST.format(
                search_by="title", sort_field="RANDOM()", sort_order="ASC"
            ),
            (
                search_pattern,
                genre,
                availability,
                user_id,
                params["books_per_page"],
                offset,
            ),
        )

    @staticmethod
    def get_total_book_count(user_id, params) -> dict[str, int]:
        """
        Retrieve the total number of books based on search, genre, and availability filters.

        Args:
            user_id (str): user_id of the user to prevent getting books that the current user owns.
            params (dict): A dictionary of query parameters. Expected keys include:
                - "search_value" (str): The value to search for.
                - "genre" (str): The genre or category of books to filter by.
                - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".

        Returns:
             dict: A dictionary containing the total number of books that match the given search, genre, and availability filters.
        """

        db = current_app.extensions["db"]

        # Search is 'Contains'
        search_pattern = f"%{params['search_value']}%"

        genre = "%%" if params["genre"] == "all genres" else f"{params['genre']}"
        availability = (
            "%%" if params["availability"] == "all" else f"{params['availability']}"
        )

        return db.fetch_one(
            BookQueries.GET_BOOK_COUNT_FOR_BOOK_LIST.format(search_by="title"),
            (
                search_pattern,
                genre,
                availability,
                user_id,
            ),
        )

    @staticmethod
    def get_book_genres() -> list[dict[str, str]]:
        """
        Retrieve a list of available genres.

        Returns:
             dict[str, str]: A dictionary containing the list of available genres.
        """

        db = current_app.extensions["db"]

        return db.fetch_all(
            CommonQueries.GET_COLUMNS_FROM_TABLE.format(
                columns="book_genre_name",
                table="book_genres",
                order_column="book_genre_name",
            )
        )

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
                - times_rented (int): Number of times the book is rented
                - owner_user_id (str): The id of the book owner
        """
        db = current_app.extensions["db"]

        params = (book_id,)

        return db.fetch_one(BookQueries.GET_BOOK_DETAILS, params)

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

        params = (book_id,)

        return db.fetch_all(BookQueries.GET_BOOK_IMAGES, params)

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

        return db.fetch_all(BookQueries.GET_RENTED_BOOKS, params)

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

        return db.fetch_all(BookQueries.GET_BOUGHT_BOOKS, params)

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

        return db.fetch_all(BookQueries.GET_LENT_BOOKS, params)

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

        return db.fetch_all(BookQueries.GET_SOLD_BOOKS, params)
