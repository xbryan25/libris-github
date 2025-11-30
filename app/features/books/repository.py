from app.db.queries import BookQueries, CommonQueries

from flask import current_app
from typing import Any, Optional


class BookRepository:
    @staticmethod
    def _build_price_filter(
        min_price: Optional[float], max_price: Optional[float], availability: str
    ) -> str:
        """
        Build a SQL price filter clause based on min/max price and availability type.
        Note: Price values are validated in the controller before reaching here, so it's safe to format them.

        Args:
            min_price: Minimum price filter (None if not set)
            max_price: Maximum price filter (None if not set)
            availability: Book availability type ('rent', 'purchase', 'both', or 'all')

        Returns:
            SQL WHERE clause fragment for price filtering
        """
        if min_price is None and max_price is None:
            return ""

        if availability == "rent":
            price_field = "b.daily_rent_price"

        elif availability == "purchase":
            price_field = "b.purchase_price"

        elif availability in ("both", "all"):
            conditions = []
            if min_price is not None and max_price is not None:
                conditions.append(
                    f"(b.daily_rent_price >= {min_price} AND b.daily_rent_price <= {max_price})"
                )
                conditions.append(
                    f"(b.purchase_price >= {min_price} AND b.purchase_price <= {max_price})"
                )
            elif min_price is not None:
                conditions.append(f"b.daily_rent_price >= {min_price}")
                conditions.append(f"b.purchase_price >= {min_price}")
            elif max_price is not None:
                conditions.append(f"b.daily_rent_price <= {max_price}")
                conditions.append(f"b.purchase_price <= {max_price}")

            if conditions:
                return f"AND ({' OR '.join(conditions)}) "
            return ""
        else:
            return ""

        conditions = []
        if min_price is not None:
            conditions.append(f"{price_field} >= {min_price}")
        if max_price is not None:
            conditions.append(f"{price_field} <= {max_price}")

        if conditions:
            return f"AND ({' AND '.join(conditions)}) "
        return ""

    @staticmethod
    def _build_distance_filter(
        mile_radius: Optional[float],
        user_lat: Optional[float],
        user_lng: Optional[float],
    ) -> str:
        """
        Build a SQL distance filter clause using Haversine formula.
        Note: Values are validated in the controller before reaching here.

        Args:
            mile_radius: Maximum distance in miles (None if not set)
            user_lat: User's latitude (None if not set)
            user_lng: User's longitude (None if not set)

        Returns:
            SQL WHERE clause fragment for distance filtering
        """
        if mile_radius is None or user_lat is None or user_lng is None:
            return ""

        # Haversine formula for distance calculation in miles
        # Earth's radius in miles: 3959
        # Formula: distance = 2 * 3959 * asin(sqrt(sin²((lat2-lat1)/2) + cos(lat1) * cos(lat2) * sin²((lng2-lng1)/2)))
        # We'll use PostgreSQL's point type and distance operator for better performance
        # But since we're using numeric lat/lng, we'll use the Haversine formula directly

        # Convert miles to approximate degrees (rough approximation: 1 degree ≈ 69 miles)
        # More accurate: use the full Haversine formula
        distance_condition = (
            f"3959 * acos(cos(radians({user_lat})) * cos(radians(ua.latitude)) * "
            f"cos(radians(ua.longitude) - radians({user_lng})) + "
            f"sin(radians({user_lat})) * sin(radians(ua.latitude))) <= {mile_radius}"
        )

        return f"AND ua.latitude IS NOT NULL AND ua.longitude IS NOT NULL AND ({distance_condition}) "

    @staticmethod
    def get_books_for_book_list(
        params, get_books_from_a_specific_user
    ) -> list[dict[str, str]]:
        """
        Retrieve a paginated list of books based on search, genre, and availability filters.

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

        # Build price filter clause
        price_filter = BookRepository._build_price_filter(
            params.get("min_price"), params.get("max_price"), params["availability"]
        )

        # Build distance filter clause
        distance_filter = BookRepository._build_distance_filter(
            params.get("mile_radius"),
            params.get("user_lat"),
            params.get("user_lng"),
        )

        # Both fetches are randomized

        if get_books_from_a_specific_user:
            return db.fetch_all(
                BookQueries.GET_BOOKS_FOR_BOOK_LIST_FROM_A_SPECIFIC_USER.format(
                    search_by="title",
                    sort_field="RANDOM()",
                    sort_order="ASC",
                    price_filter=price_filter,
                    distance_filter=distance_filter,
                ),
                (
                    search_pattern,
                    availability,
                    params["user_id"],
                    genre,
                    genre,
                    params["books_per_page"],
                    offset,
                ),
            )

        else:
            return db.fetch_all(
                BookQueries.GET_BOOKS_FOR_BOOK_LIST.format(
                    search_by="title",
                    sort_field="RANDOM()",
                    sort_order="ASC",
                    price_filter=price_filter,
                    distance_filter=distance_filter,
                ),
                (
                    search_pattern,
                    availability,
                    params["user_id"],
                    genre,
                    genre,
                    params["books_per_page"],
                    offset,
                ),
            )

    @staticmethod
    def get_total_book_count(
        params, get_book_count_from_a_specific_user
    ) -> dict[str, int]:
        """
        Retrieve the total number of books based on search, genre, and availability filters.

        Args:
            params (dict): A dictionary of query parameters. Expected keys include:
                - "search_value" (str): The value to search for.
                - "genre" (str): The genre or category of books to filter by.
                - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".
                - "user_id" (str): user_id of the user to prevent counting books that the current user owns, or, if from other
                                    user, count all books that that user owns
            get_book_count_from_a_specific_user (bool): A boolean value that determine whether the books counted will be from
                                                        everyone or only from a specific user

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

        # Build price filter clause
        price_filter = BookRepository._build_price_filter(
            params.get("min_price"), params.get("max_price"), params["availability"]
        )

        # Build distance filter clause
        distance_filter = BookRepository._build_distance_filter(
            params.get("mile_radius"),
            params.get("user_lat"),
            params.get("user_lng"),
        )

        if get_book_count_from_a_specific_user:
            return db.fetch_one(
                BookQueries.GET_BOOK_COUNT_FOR_BOOK_LIST_FROM_A_SPECIFIC_USER.format(
                    search_by="title",
                    price_filter=price_filter,
                    distance_filter=distance_filter,
                ),
                (
                    search_pattern,
                    genre,
                    availability,
                    params["user_id"],
                ),
            )

        else:
            return db.fetch_one(
                BookQueries.GET_BOOK_COUNT_FOR_BOOK_LIST.format(
                    search_by="title",
                    price_filter=price_filter,
                    distance_filter=distance_filter,
                ),
                (
                    search_pattern,
                    genre,
                    availability,
                    params["user_id"],
                ),
            )

    @staticmethod
    def get_my_library_books(user_id, params) -> list[dict[str, str]]:
        """
        Retrieve a paginated list of books based on search, genre, and availability filters.

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
            BookQueries.GET_MY_LIBRARY_BOOKS.format(
                search_by="title", sort_field="RANDOM()", sort_order="ASC"
            ),
            (
                search_pattern,
                availability,
                user_id,
                genre,
                genre,
                params["books_per_page"],
                offset,
            ),
        )

    @staticmethod
    def get_total_my_library_book_count(user_id, params) -> dict[str, int]:
        """
        Retrieve the total number of books based on search, genre, and availability filters.

        Args:
            params (dict): A dictionary of query parameters. Expected keys include:
                - "search_value" (str): The value to search for.
                - "genre" (str): The genre or category of books to filter by.
                - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".
                - "user_id" (str): user_id of the user to prevent counting books that the current user owns, or, if from other
                                    user, count all books that that user owns
            get_book_count_from_a_specific_user (bool): A boolean value that determine whether the books counted will be from
                                                        everyone or only from a specific user

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
            BookQueries.GET_MY_LIBRARY_BOOK_COUNT.format(search_by="title"),
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

    @staticmethod
    def add_new_book(user_id, book_data) -> dict[str, str]:
        """
        to be written
        """

        db = current_app.extensions["db"]

        params = (
            book_data["title"],
            book_data["author"],
            book_data["condition"],
            book_data["description"],
            book_data["availability"],
            book_data["daily_rent_price"],
            book_data["security_deposit"],
            book_data["purchase_price"],
            user_id,
        )

        return db.execute_query_returning(BookQueries.ADD_NEW_BOOK, params)

    @staticmethod
    def edit_a_book(book_id, book_data) -> dict[str, str]:
        """
        to be written
        """

        db = current_app.extensions["db"]

        params = (
            book_data["title"],
            book_data["author"],
            book_data["condition"],
            book_data["description"],
            book_data["availability"],
            book_data["daily_rent_price"],
            book_data["security_deposit"],
            book_data["purchase_price"],
            book_id,
        )

        return db.execute_query(BookQueries.EDIT_A_BOOK, params)

    @staticmethod
    def get_genre_ids_from_genre_names(genres) -> list[dict[str, str]]:
        db = current_app.extensions["db"]

        return db.fetch_all(
            CommonQueries.GET_IDS_BY_VALUES.format(
                table="book_genres", column="book_genre_id", field="book_genre_name"
            ),
            (genres,),
        )

    @staticmethod
    def connect_book_to_genres(book_id, genres) -> None:
        """
        to be written
        """

        db = current_app.extensions["db"]

        genre_ids = BookRepository.get_genre_ids_from_genre_names(genres)

        for genre_id in genre_ids:
            db.execute_query(
                BookQueries.INSERT_TO_BOOK_GENRE_LINKS,
                (book_id, genre_id["book_genre_id"]),
            )

    @staticmethod
    def remove_connection_of_book_to_genres(book_id, genres) -> None:
        """
        to be written
        """

        db = current_app.extensions["db"]

        genre_ids = BookRepository.get_genre_ids_from_genre_names(genres)

        for genre_id in genre_ids:
            db.execute_query(
                BookQueries.DELETE_FROM_BOOK_GENRE_LINKS,
                (book_id, genre_id["book_genre_id"]),
            )

    @staticmethod
    def add_book_images_to_database(
        book_id, uploaded_urls, add_type="add_book"
    ) -> None:
        """
        to be written
        """

        db = current_app.extensions["db"]

        if add_type == "add_book":
            for index, uploaded_url in enumerate(uploaded_urls):
                db.execute_query(
                    BookQueries.INSERT_TO_BOOK_IMAGES,
                    (
                        uploaded_url["image_url"],
                        uploaded_url["uploaded_at"],
                        index + 1,
                        book_id,
                    ),
                )

        else:
            for uploaded_url_with_order_num in uploaded_urls:
                db.execute_query(
                    BookQueries.INSERT_TO_BOOK_IMAGES,
                    (
                        uploaded_url_with_order_num[1]["image_url"],
                        uploaded_url_with_order_num[1]["uploaded_at"],
                        uploaded_url_with_order_num[0],
                        book_id,
                    ),
                )

    @staticmethod
    def remove_book_images_from_database(
        book_id, existing_book_image_urls_to_delete
    ) -> None:
        """
        to be written
        """

        db = current_app.extensions["db"]

        for existing_book_image_url_to_delete in existing_book_image_urls_to_delete:
            db.execute_query(
                BookQueries.REMOVE_FROM_BOOK_IMAGES,
                (book_id, existing_book_image_url_to_delete),
            )

    @staticmethod
    def edit_book_order_in_database(book_id, order_num, image_url) -> None:
        """
        to be written
        """

        db = current_app.extensions["db"]

        db.execute_query(
            BookQueries.EDIT_BOOK_ORDER_IN_BOOK_IMAGES,
            (order_num, book_id, image_url),
        )

    @staticmethod
    def delete_all_book_genre_links_from_book(book_id) -> None:
        """
        to be written
        """

        db = current_app.extensions["db"]

        db.execute_query(
            CommonQueries.DELETE_BY_ID.format(table="book_genre_links", pk="book_id"),
            (book_id,),
        )

    @staticmethod
    def check_if_book_has_rent_or_purchase_history(book_id) -> bool:
        """
        to be written
        """

        db = current_app.extensions["db"]

        row = db.fetch_one(
            BookQueries.CHECK_IF_BOOK_HAS_RENT_OR_PURCHASE_HISTORY,
            (book_id, book_id),
        )

        if row:
            return True
        else:
            return False

    @staticmethod
    def soft_delete_a_book(book_id) -> None:
        """
        to be written
        """

        db = current_app.extensions["db"]

        db.execute_query(
            BookQueries.SOFT_DELETE_A_BOOK,
            (True, book_id),
        )

    @staticmethod
    def delete_a_book(book_id) -> None:
        """
        to be written
        """

        db = current_app.extensions["db"]

        db.execute_query(
            BookQueries.DELETE_A_BOOK,
            (book_id,),
        )
