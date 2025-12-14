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
    def get_books_for_book_list_controller() -> tuple[Response, int]:
        """Retrieve details of different books based on pagination, optional search, genre, and availability filters."""

        ALLOWED_AVAILABILITY_FILTERS = {"for rent", "for sale", "both", "all"}

        get_books_from_a_specific_user = False

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
                "user_id": request.args.get("userId"),
                "min_price": request.args.get("minPrice"),
                "max_price": request.args.get("maxPrice"),
                "km_radius": request.args.get("kmRadius"),
                "user_lat": request.args.get("userLat"),
                "user_lng": request.args.get("userLng"),
            }

            try:
                min_price = float(params["min_price"]) if params["min_price"] else None
                max_price = float(params["max_price"]) if params["max_price"] else None
            except ValueError:
                raise InvalidParameterError(
                    "Price filter values ('minPrice', 'maxPrice') must be valid numbers."
                )

            params["min_price"] = min_price
            params["max_price"] = max_price

            if (min_price is not None and min_price < 0) or (
                max_price is not None and max_price < 0
            ):
                raise InvalidParameterError("Price values must be non-negative.")

            if (
                min_price is not None
                and max_price is not None
                and min_price > max_price
            ):
                raise InvalidParameterError(
                    "Minimum price cannot be greater than maximum price."
                )

            # Validate and parse distance filter parameters
            try:
                km_radius = float(params["km_radius"]) if params["km_radius"] else None
                user_lat = float(params["user_lat"]) if params["user_lat"] else None
                user_lng = float(params["user_lng"]) if params["user_lng"] else None
            except ValueError:
                raise InvalidParameterError(
                    "Distance filter values ('kmRadius', 'userLat', 'userLng') must be valid numbers."
                )

            params["km_radius"] = km_radius
            params["user_lat"] = user_lat
            params["user_lng"] = user_lng

            # Validate latitude and longitude ranges
            if user_lat is not None and (user_lat < -90 or user_lat > 90):
                raise InvalidParameterError("Latitude must be between -90 and 90.")

            if user_lng is not None and (user_lng < -180 or user_lng > 180):
                raise InvalidParameterError("Longitude must be between -180 and 180.")

            if km_radius is not None and km_radius < 0:
                raise InvalidParameterError("km radius must be non-negative.")

            # If km radius is set, user location must be provided
            if km_radius is not None and (user_lat is None or user_lng is None):
                raise InvalidParameterError(
                    "User location (userLat, userLng) is required when kmRadius is specified."
                )

            if params["user_id"]:
                get_books_from_a_specific_user = True
            else:
                params["user_id"] = user_id

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

            books = BookServices.get_books_for_book_list_service(
                params, get_books_from_a_specific_user
            )

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

        get_book_count_from_a_specific_user = False

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
                "user_id": request.args.get("userId"),
                "min_price": request.args.get("minPrice"),
                "max_price": request.args.get("maxPrice"),
                "km_radius": request.args.get("kmRadius"),
                "user_lat": request.args.get("userLat"),
                "user_lng": request.args.get("userLng"),
            }

            try:
                min_price = float(params["min_price"]) if params["min_price"] else None
                max_price = float(params["max_price"]) if params["max_price"] else None
            except ValueError:
                raise InvalidParameterError(
                    "Price filter values ('minPrice', 'maxPrice') must be valid numbers."
                )

            params["min_price"] = min_price
            params["max_price"] = max_price

            if (min_price is not None and min_price < 0) or (
                max_price is not None and max_price < 0
            ):
                raise InvalidParameterError("Price values must be non-negative.")

            if (
                min_price is not None
                and max_price is not None
                and min_price > max_price
            ):
                raise InvalidParameterError(
                    "Minimum price cannot be greater than maximum price."
                )

            # Validate and parse distance filter parameters
            try:
                km_radius = float(params["km_radius"]) if params["km_radius"] else None
                user_lat = float(params["user_lat"]) if params["user_lat"] else None
                user_lng = float(params["user_lng"]) if params["user_lng"] else None
            except ValueError:
                raise InvalidParameterError(
                    "Distance filter values ('kmRadius', 'userLat', 'userLng') must be valid numbers."
                )

            params["km_radius"] = km_radius
            params["user_lat"] = user_lat
            params["user_lng"] = user_lng

            # Validate latitude and longitude ranges
            if user_lat is not None and (user_lat < -90 or user_lat > 90):
                raise InvalidParameterError("Latitude must be between -90 and 90.")

            if user_lng is not None and (user_lng < -180 or user_lng > 180):
                raise InvalidParameterError("Longitude must be between -180 and 180.")

            if km_radius is not None and km_radius < 0:
                raise InvalidParameterError("km radius must be non-negative.")

            # If km radius is set, user location must be provided
            if km_radius is not None and (user_lat is None or user_lng is None):
                raise InvalidParameterError(
                    "User location (userLat, userLng) is required when kmRadius is specified."
                )

            if params["user_id"]:
                get_book_count_from_a_specific_user = True
            else:
                params["user_id"] = user_id

            if params["availability"] not in ALLOWED_AVAILABILITY_FILTERS:
                raise InvalidParameterError(
                    f"""Invalid 'availability' value: '{params['availability']}'.
                    Must be one of: ['for rent', 'for sale', 'both', 'all']."""
                )

            total_book_count = BookServices.get_total_book_count_service(
                params, get_book_count_from_a_specific_user
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
    def get_my_library_books_controller() -> tuple[Response, int]:
        """Retrieve details of different books based on pagination,
        optional search, genre, and availability filters, including price."""

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
                "min_price": request.args.get("minPrice"),
                "max_price": request.args.get("maxPrice"),
            }

            try:
                min_price = float(params["min_price"]) if params["min_price"] else None
                max_price = float(params["max_price"]) if params["max_price"] else None
            except ValueError:
                raise InvalidParameterError(
                    "Price filter values ('minPrice', 'maxPrice') must be valid numbers."
                )

            params["min_price"] = min_price
            params["max_price"] = max_price

            if (min_price is not None and min_price < 0) or (
                max_price is not None and max_price < 0
            ):
                raise InvalidParameterError("Price values must be non-negative.")

            if (
                min_price is not None
                and max_price is not None
                and min_price > max_price
            ):
                raise InvalidParameterError(
                    "Minimum price cannot be greater than maximum price."
                )

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

            my_library_books = BookServices.get_my_library_books_service(
                user_id, params
            )

            return (
                jsonify(
                    [
                        dict_keys_to_camel(
                            cast(
                                dict[str, Any],
                                asdict_enum_safe(my_library_book_details),
                            )
                        )
                        for my_library_book_details in my_library_books
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
    def get_total_my_library_book_count_controller() -> tuple[Response, int]:
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

            total_book_count = BookServices.get_total_my_library_book_count_service(
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

    @staticmethod
    def add_new_book_controller() -> tuple[Response, int]:
        """(add later)"""

        try:
            book_data = {
                "title": request.form.get("title", "-"),
                "author": request.form.get("author", "-"),
                "condition": request.form.get("condition", "-"),
                "genres": request.form.getlist("genres"),
                "description": request.form.get("description", "-"),
                "availability": request.form.get("availability", "-"),
                "daily_rent_price": int(request.form.get("dailyRentPrice", 0) or 0),
                "security_deposit": int(request.form.get("securityDeposit", 0) or 0),
                "purchase_price": int(request.form.get("purchasePrice", 0) or 0),
                "rental_duration": int(request.form.get("rentalDuration", 0) or 0),
            }

            book_images = request.files

            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            BookServices.add_new_book_service(user_id, book_data, book_images)

            return (
                jsonify({"message": f"'{book_data['title']}' added successfully."}),
                200,
            )
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def edit_a_book_controller(book_id: str) -> tuple[Response, int]:
        """(add later)"""

        try:
            book_data = {
                "title": request.form.get("title", "-"),
                "author": request.form.get("author", "-"),
                "condition": request.form.get("condition", "-"),
                "genres_to_add": request.form.getlist("genresToAdd"),
                "genres_to_delete": request.form.getlist("genresToDelete"),
                "existing_book_image_urls": request.form.getlist(
                    "existingBookImageUrls"
                ),
                "existing_book_image_urls_to_delete": request.form.getlist(
                    "existingBookImageUrlsToDelete"
                ),
                "all_book_order": request.form.getlist("allBookOrder"),
                "description": request.form.get("description", "-"),
                "availability": request.form.get("availability", "-"),
                "daily_rent_price": int(request.form.get("dailyRentPrice", 0) or 0),
                "security_deposit": int(request.form.get("securityDeposit", 0) or 0),
                "purchase_price": int(request.form.get("purchasePrice", 0) or 0),
                "rental_duration": int(request.form.get("rentalDuration", 0) or 0),
            }

            book_images = request.files

            BookServices.edit_a_book_service(book_id, book_data, book_images)

            return (
                jsonify(
                    {"message": f"'{book_data['title']}' was edited successfully."}
                ),
                200,
            )
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_a_book_controller(book_id: str) -> tuple[Response, int]:
        """(add later)"""

        try:
            book_details = request.get_json()

            title = book_details.get("title")

            BookServices.delete_a_book_service(book_id)

            return (
                jsonify({"message": f"{title} was edited successfully."}),
                200,
            )
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
