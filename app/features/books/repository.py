from app.db.queries import BookQueries

from flask import current_app


class BookRepository:
    @staticmethod
    def get_many_books(user_id, params) -> list[dict[str, str]]:
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
            BookQueries.GET_MANY_BOOKS.format(
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
            BookQueries.GET_BOOKS_COUNT.format(search_by="title"),
            (
                search_pattern,
                genre,
                availability,
                user_id,
            ),
        )
