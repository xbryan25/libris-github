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

            genre: The primary genre of the book.

            availability: The availability status of the book — can be "For Rent", "For Sale", or "Both".

            daily_rent_price: The daily rent price of the book.

            purchase_price: The purchase price of the book.

            owner_username: The username of the user in which the book belongs to.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return BookControllers.get_many_books_controller()
