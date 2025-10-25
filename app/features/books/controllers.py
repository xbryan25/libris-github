from flask import request, jsonify, Response

import traceback

from flask_jwt_extended import get_jwt_identity

from .services import BookServices

from app.exceptions.custom_exceptions import InvalidParameterError

from app.utils import dict_keys_to_camel, asdict_enum_safe

from typing import Any, cast

# from psycopg.errors import UniqueViolation, ForeignKeyViolation


class BookControllers:

    @staticmethod
    def get_user_books_controller() -> tuple[Response, int]:
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
    def get_many_books_controller() -> tuple[Response, int]:
        """Retrieve details of different books based on pagination, optional search, genre, and availability filters."""

        ALLOWED_AVAILABILITY_FILTERS = {"for rent", "for sale", "both", "all"}

        try:

            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"message": "Not authenticated."}), 401

            params = {
                "books_per_page": int(request.args.get("booksPerPage", 0)),
                "page_number": int(request.args.get("pageNumber", 0)),
                "search_value": (request.args.get("searchValue") or "").strip(),
                "genre": request.args.get("bookGenre", "all genres").lower(),
                "availability": request.args.get(
                    "bookAvailability", "for rent"
                ).lower(),
            }

            if params["books_per_page"] < 0:
                raise InvalidParameterError(
                    f"Invalid 'booksPerPage' value: '{params['books_per_page']}'. Must be a positive integer."
                )

            if params["page_number"] < 0:
                raise InvalidParameterError(
                    f"Invalid 'pageNumber' value: '{params['page_number']}'. Must be a positive integer."
                )

            if params["availability"] not in ALLOWED_AVAILABILITY_FILTERS:
                raise InvalidParameterError(
                    f"""Invalid 'availability' value: '{params['availability']}'.
                    Must be one of: ['for rent', 'for sale', 'both', 'all']."""
                )

            books = BookServices.get_many_books_service(user_id, params)

            return (
                jsonify(
                    [
                        dict_keys_to_camel(
                            cast(dict[str, Any], asdict_enum_safe(book_details))
                        )
                        for book_details in books
                    ]
                ),
                200,
            )

        except InvalidParameterError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except (ValueError, TypeError):
            traceback.print_exc()
            return (
                jsonify(
                    {
                        "error": "Invalid query parameter. 'rowsPerPage' and 'pageNumber' must be positive integers."
                    }
                ),
                400,
            )

    @staticmethod
    def get_total_book_count_controller() -> tuple[Response, int]:
        """Retrieve the total count of books based on pagination, optional search, genre, and availability filters."""

        ALLOWED_AVAILABILITY_FILTERS = {"for rent", "for sale", "both", "all"}

        try:

            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated."}), 401

            params = {
                "search_value": (request.args.get("searchValue") or "").strip(),
                "genre": request.args.get("bookGenre", "all genres").lower(),
                "availability": request.args.get(
                    "bookAvailability", "for rent"
                ).lower(),
            }

            if params["availability"] not in ALLOWED_AVAILABILITY_FILTERS:
                raise InvalidParameterError(
                    f"""Invalid 'availability' value: '{params['availability']}'.
                    Must be one of: ['for rent', 'for sale', 'both', 'all']."""
                )

            total_book_count = BookServices.get_total_book_count_service(
                user_id, params
            )

            return jsonify({"totalCount": total_book_count}), 200

        except InvalidParameterError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except (ValueError, TypeError):
            traceback.print_exc()
            return (
                jsonify(
                    {
                        "error": "Invalid query parameter. 'rowsPerPage' and 'pageNumber' must be positive integers."
                    }
                ),
                400,
            )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_book_genres_controller() -> tuple[Response, int]:
        """Retrieve the a list of available genres."""

        try:

            book_genres = BookServices.get_book_genres_service()
            return jsonify(book_genres), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_renting_books_controller() -> tuple[Response, int]:
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
    def get_bought_books_controller() -> tuple[Response, int]:
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
    def get_lent_controller() -> tuple[Response, int]:
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
    def get_sold_controller() -> tuple[Response, int]:
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
    def get_book_details_controller(book_id: str) -> tuple[Response, int]:
        try:
            book_details = BookServices.get_book_details_service(book_id)

            if not book_details:
                return jsonify({"error": "Book not found"}), 404

            return jsonify(book_details), 200
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
