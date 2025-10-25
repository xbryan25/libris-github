from flask import Blueprint, Response
from .controllers import BookControllers
from flask_jwt_extended import jwt_required

books_bp = Blueprint("books_bp", __name__)


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


@books_bp.route("/books/<string:book_id>", methods=["GET"])
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
