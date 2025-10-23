from typing import Any, Optional
from .repository import BookRepository
from app.utils.date_utils import DateUtils


class BookServices:
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
