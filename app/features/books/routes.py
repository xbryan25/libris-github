from flask import Blueprint, Response
from .controllers import BookControllers

from flask_jwt_extended import jwt_required

books_bp = Blueprint("books_bp", __name__)


@books_bp.route("/", methods=["GET"])
@jwt_required()
def get_many_books() -> tuple[Response, int]:
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

    return BookControllers.get_many_books_controller()


@books_bp.route("/total-count", methods=["GET"])
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
