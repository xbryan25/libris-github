from flask import Blueprint, Response
from .controllers import BookControllers

from flask_jwt_extended import jwt_required

books_bp = Blueprint("books_bp", __name__)


@books_bp.route("/book-list-books", methods=["GET"])
@jwt_required()
def get_books_for_book_list() -> tuple[Response, int]:
    """
    Retrieve details of different books based on pagination, optional search, genre, and availability filters.

    This endpoint requires authentication via a valid access token (HTTP-only cookie).
    It returns the details of different books, filtered by pagination and optionally by search, genre,
    and availability.

    Query parameters:

        booksPerPage: The number of book details to retrieve.

        pageNumber: This number will be multiplied by booksPerPage then serve as the offset for pagination.

        searchValue: The value to search for (optional).

        genre: The genre or category of books to filter by.

        availability: The availability status of the book — can be "For Rent", "For Sale", or "Both".

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        bookDetails: An array of book details objects with the following fields:

            title: The title of the book.

            author: The author of the book.

            bookGenre: The primary genre of the book.

            bookAvailability: The availability status of the book — can be "For Rent", "For Sale", or "Both".

            daily_rent_price: The daily rent price of the book.

            purchase_price: The purchase price of the book.

            owner_username: The username of the user in which the book belongs to.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return BookControllers.get_books_for_book_list_controller()


@books_bp.route("/my-library-books", methods=["GET"])
@jwt_required()
def get_my_library_books() -> tuple[Response, int]:
    """
    Retrieve details of different books based on pagination, optional search, genre, and availability filters.

    This endpoint requires authentication via a valid access token (HTTP-only cookie).
    It returns the details of different books, filtered by pagination and optionally by search, genre,
    and availability.

    Query parameters:

        booksPerPage: The number of book details to retrieve.

        pageNumber: This number will be multiplied by booksPerPage then serve as the offset for pagination.

        searchValue: The value to search for (optional).

        genre: The genre or category of books to filter by.

        availability: The availability status of the book — can be "For Rent", "For Sale", or "Both".

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        bookDetails: An array of book details objects with the following fields:

            title: The title of the book.

            author: The author of the book.

            bookGenre: The genre of the book.

            bookAvailability: The availability status of the book — can be "For Rent", "For Sale", or "Both".

            daily_rent_price: The daily rent price of the book.

            purchase_price: The purchase price of the book.


    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return BookControllers.get_my_library_books_controller()


@books_bp.route("/my-library-books-count", methods=["GET"])
@jwt_required()
def get_total_my_library_book_count() -> tuple[Response, int]:
    """
    Retrieve the total number of books based on pagination, optional search, genre, and availability filters.

    This endpoint requires authentication via a valid access token (HTTP-only cookie).
    It returns the total count books, filtered by pagination and optionally by search, genre,
    and availability.

    Query parameters:

        searchValue: The value to search for (optional).

        bookGenre: The genre or category of books to filter by.

        bookAvailability: The availability status of the book — can be "For Rent", "For Sale", or "Both".

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        totalCount: The total number of students matching the provided filters.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return BookControllers.get_total_my_library_book_count_controller()


@books_bp.route("/book-list-books-count", methods=["GET"])
@jwt_required()
def get_total_book_count() -> tuple[Response, int]:
    """
    Retrieve the total number of books based on pagination, optional search, genre, and availability filters.

    This endpoint requires authentication via a valid access token (HTTP-only cookie).
    It returns the total count books, filtered by pagination and optionally by search, genre,
    and availability.

    Query parameters:

        searchValue: The value to search for (optional).

        bookGenre: The genre or category of books to filter by.

        bookAvailability: The availability status of the book — can be "For Rent", "For Sale", or "Both".

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        totalCount: The total number of students matching the provided filters.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return BookControllers.get_total_book_count_controller()


@books_bp.route("/book-genres", methods=["GET"])
@jwt_required()
def get_book_genres() -> tuple[Response, int]:
    """
    Retrieve all book genres.

    This endpoint requires authentication via a valid access token (HTTP-only cookie).
    It returns a list of all available book genres.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        [str]: A list containing all available book genres.

    Possible errors:
        401: If the user is not authenticated or the token is invalid.
        500 if an unexpected error occurs during processing.
    """

    return BookControllers.get_book_genres_controller()


@books_bp.route("/my-books", methods=["GET"])
@jwt_required()
def get_user_books() -> tuple[Response, int]:
    """
    Retrieve all books data for the authenticated user.

    This endpoint returns books in four categories:
    - renting: Books currently being rented by the user
    - bought: Books purchased by the user
    - rented-by-others: Books owned by user that are rented by others
    - bought-by-others: Books owned by user that were purchased by others

    Response JSON:
        {
            "renting": [...],
            "bought": [...],
            "rented-by-others": [...],
            "bought-by-others": [...]
        }

    Possible errors:
        401 if the user is not authenticated
        500 if an unexpected error occurs
    """
    return BookControllers.get_user_books_controller()


@books_bp.route("/my-books/renting", methods=["GET"])
@jwt_required()
def get_renting_books() -> tuple[Response, int]:
    """
    Retrieve books currently being rented by the authenticated user.

    Response JSON:
        {
            "renting": [
                {
                    "id": 1,
                    "title": "Book Title",
                    "author": "Author Name",
                    "image": "image_url",
                    "from": "owner_username",
                    "returnDate": "October 1, 2025",
                    "cost": "50"
                }
            ]
        }

    Possible errors:
        401 if the user is not authenticated
        500 if an unexpected error occurs
    """
    return BookControllers.get_renting_books_controller()


@books_bp.route("/my-books/bought", methods=["GET"])
@jwt_required()
def get_bought_books() -> tuple[Response, int]:
    """
    Retrieve books purchased by the authenticated user.

    Response JSON:
        {
            "bought": [
                {
                    "id": 1,
                    "title": "Book Title",
                    "author": "Author Name",
                    "image": "image_url",
                    "from": "owner_username",
                    "cost": "50"
                }
            ]
        }

    Possible errors:
        401 if the user is not authenticated
        500 if an unexpected error occurs
    """
    return BookControllers.get_bought_books_controller()


@books_bp.route("/my-books/lent", methods=["GET"])
@jwt_required()
def get_rented_by_others() -> tuple[Response, int]:
    """
    Retrieve books owned by the user that are currently rented by others.

    Response JSON:
        {
            "rented-by-others": [
                {
                    "id": 1,
                    "title": "Book Title",
                    "author": "Author Name",
                    "image": "image_url",
                    "by": "renter_username",
                    "returnDate": "October 1, 2025",
                    "cost": "50"
                }
            ]
        }

    Possible errors:
        401 if the user is not authenticated
        500 if an unexpected error occurs
    """
    return BookControllers.get_lent_controller()


@books_bp.route("/my-books/sold", methods=["GET"])
@jwt_required()
def get_bought_by_others() -> tuple[Response, int]:
    """
    Retrieve books owned by the user that were purchased by others.

    Response JSON:
        {
            "bought-by-others": [
                {
                    "id": 1,
                    "title": "Book Title",
                    "author": "Author Name",
                    "image": "image_url",
                    "by": "buyer_username",
                    "cost": "50"
                }
            ]
        }

    Possible errors:
        401 if the user is not authenticated
        500 if an unexpected error occurs
    """
    return BookControllers.get_sold_controller()


@books_bp.route("/<string:book_id>", methods=["GET"])
@jwt_required()
def get_book_details(book_id: str) -> tuple[Response, int]:
    """
    Retrieve detailed information about a specific book.

    Path parameters:
        book_id (string): The UUID of the book

    Response JSON:
        {
            "book_id": "uuid",
            "title": "Book Title",
            "author": "Author Name",
            "genre": "Genre",
            "condition": "new",
            "description": "Book description",
            "availability": "both",
            "daily_rent_price": 5,
            "security_deposit": 20,
            "purchase_price": 50,
            "owner_username": "username",
            "owner_trust_score": 95,
            "images": ["url1", "url2"]
        }

    Possible errors:
        404 if the book is not found
        500 if an unexpected error occurs
    """
    return BookControllers.get_book_details_controller(book_id)
