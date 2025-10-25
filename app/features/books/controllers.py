from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from .services import BookServices
import traceback


class BookControllers:
    @staticmethod
    def get_user_books_controller() -> tuple[dict, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            books_data = BookServices.get_all_user_books_service(user_id)
            return jsonify(books_data), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_renting_books_controller() -> tuple[dict, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            renting_books = BookServices.get_renting_books_service(user_id)
            return jsonify({"renting": renting_books}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_bought_books_controller() -> tuple[dict, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            bought_books = BookServices.get_bought_books_service(user_id)
            return jsonify({"bought": bought_books}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_lent_controller() -> tuple[dict, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            rented_by_others = BookServices.get_lent_books_service(user_id)
            return jsonify({"rented-by-others": rented_by_others}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_sold_controller() -> tuple[dict, int]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            bought_by_others = BookServices.get_sold_books_service(user_id)
            return jsonify({"bought-by-others": bought_by_others}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_book_details_controller(book_id: str) -> tuple[dict, int]:
        try:
            book_details = BookServices.get_book_details_service(book_id)

            if not book_details:
                return jsonify({"error": "Book not found"}), 404

            return jsonify(book_details), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
