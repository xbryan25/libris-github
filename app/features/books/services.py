from .repository import BookRepository

from app.common.dataclasses import Book, MyLibraryBook

from app.utils.converters import convert_book_dict, convert_my_library_book_dict

from typing import Any, Optional

from app.utils import DateUtils, upload_images_to_bucket

from supabase import create_client, Client

from flask import current_app


class BookServices:

    @staticmethod
    def get_books_for_book_list_service(
        params, get_books_from_a_specific_user
    ) -> list[Book]:
        """
        Retrieve details of different books based on pagination, optional search, genre, and availability filters.

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
            list[Book]: A list of Book dataclass instances representing books_per_page books.
        """

        # Clean 'availability' values from 'for rent' to 'rent' and 'for sale' to 'purchase'
        if params["availability"] == "for rent":
            params["availability"] = "rent"
        elif params["availability"] == "for sale":
            params["availability"] = "purchase"

        books = BookRepository.get_books_for_book_list(
            params, get_books_from_a_specific_user
        )

        book_dataclasses = []

        for book in books:
            # Convert dict to dataclass before appending
            book_dataclasses.append(convert_book_dict(book))

        return book_dataclasses

    @staticmethod
    def get_total_book_count_service(
        params, get_book_count_from_a_specific_user
    ) -> int:
        """
        Retrieve the total count of books based on pagination, optional search, genre, and availability filters.

        Args:
            params (dict): A dictionary containing the optional search, genre, and availability filters.
                Expected keys include:
                    - "search_value" (str): The value to search for.
                    - "genre" (str): The genre or category of books to filter by.
                    - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".
                    - "user_id" (str): user_id of the user to prevent counting books that the current user owns, or, if from
                                        other user, count all books that that user owns
            get_book_count_from_a_specific_user (bool): A boolean value that determine whether the books counted will be
                                                        from everyoneor only from a specific user

        Returns:
            int: The total book count, with search, genre, and availability filters being optionally applied.
        """

        # Clean 'availability' values from 'for rent' to 'rent' and 'for sale' to 'purchase'
        if params["availability"] == "for rent":
            params["availability"] = "rent"
        elif params["availability"] == "for sale":
            params["availability"] = "purchase"

        return BookRepository.get_total_book_count(
            params, get_book_count_from_a_specific_user
        )["count"]

    @staticmethod
    def get_my_library_books_service(user_id, params) -> list[MyLibraryBook]:
        """
        Retrieve details of different books based on pagination, optional search, genre, and availability filters.

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
            list[MyLibraryBook]: A list of MyLibraryBook dataclass instances representing books_per_page books.
        """

        # Clean 'availability' values from 'for rent' to 'rent' and 'for sale' to 'purchase'
        if params["availability"] == "for rent":
            params["availability"] = "rent"
        elif params["availability"] == "for sale":
            params["availability"] = "purchase"

        my_library_books = BookRepository.get_my_library_books(user_id, params)

        my_library_book_dataclasses = []

        for my_library_book in my_library_books:
            # Convert dict to dataclass before appending
            my_library_book_dataclasses.append(
                convert_my_library_book_dict(my_library_book)
            )

        # print(my_library_book_dataclasses)
        return my_library_book_dataclasses

    @staticmethod
    def get_total_my_library_book_count_service(user_id, params) -> int:
        """
        Retrieve the total count of books based on pagination, optional search, genre, and availability filters.

        Args:
            params (dict): A dictionary containing the optional search, genre, and availability filters.
                Expected keys include:
                    - "search_value" (str): The value to search for.
                    - "genre" (str): The genre or category of books to filter by.
                    - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".
                    - "user_id" (str): user_id of the user to prevent counting books that the current user owns, or, if from
                                        other user, count all books that that user owns
            get_book_count_from_a_specific_user (bool): A boolean value that determine whether the books counted will be
                                                        from everyoneor only from a specific user

        Returns:
            int: The total book count, with search, genre, and availability filters being optionally applied.
        """

        # Clean 'availability' values from 'for rent' to 'rent' and 'for sale' to 'purchase'
        if params["availability"] == "for rent":
            params["availability"] = "rent"
        elif params["availability"] == "for sale":
            params["availability"] = "purchase"

        return BookRepository.get_total_my_library_book_count(user_id, params)["count"]

    @staticmethod
    def get_book_genres_service() -> list[str]:
        """
        Retrieve a list of available genres.

        Returns:
            [str]: A list containing all available book genres.
        """

        dict_book_genres: list[dict[str, str]] = BookRepository.get_book_genres()

        book_genres = [
            dict_book_genre["book_genre_name"] for dict_book_genre in dict_book_genres
        ]

        return book_genres

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
            "genres": book["genres"],
            "condition": book["condition"],
            "description": book["description"],
            "availability": book["availability"],
            "daily_rent_price": (
                int(book["daily_rent_price"]) if book["daily_rent_price"] else 0
            ),
            "security_deposit": (
                int(book["security_deposit"]) if book["security_deposit"] else 0
            ),
            "purchase_price": (
                int(book["purchase_price"]) if book["purchase_price"] else 0
            ),
            "owner_user_id": book["owner_user_id"],
            "owner_username": book["owner_username"],
            "owner_profile_picture": book["owner_profile_picture"],
            "owner_trust_score": book["owner_trust_score"],
            "times_rented": int(book["times_rented"]),
            "is_rented": book["is_rented"],
            "is_purchased": book["is_purchased"],
            "images": [img["image_url"] for img in images],
        }

    @staticmethod
    def add_new_book_service(user_id, book_data, book_images) -> None:
        """Add a new book (improve later)"""

        # Add book details to book

        book_data["condition"] = book_data["condition"].lower()

        if book_data["availability"] == "For Rent":
            book_data["availability"] = "rent"
        elif book_data["availability"] == "For Sale":
            book_data["availability"] = "purchase"
        else:
            book_data["availability"] = book_data["availability"].lower()

        book_id_dict = BookRepository.add_new_book(user_id, book_data)

        book_id = book_id_dict["book_id"]

        # Link to book_genre_links table

        BookRepository.connect_book_to_genres(book_id, book_data["genres"])

        # Upload images to Supabase

        parsed_book_images = book_images.getlist("bookImages")

        supabase: Client = create_client(
            current_app.config.get("SUPABASE_URL"),
            current_app.config.get("SUPABASE_SERVICE_KEY"),
        )

        bucket_name = "book_images"

        uploaded_urls = upload_images_to_bucket(
            supabase, parsed_book_images, book_id, bucket_name
        )

        BookRepository.add_book_images_to_database(book_id, uploaded_urls)

    @staticmethod
    def edit_a_book_service(book_id, book_data, book_images) -> None:
        """Add a new book (improve later)"""

        # Update details of the book
        book_data["condition"] = book_data["condition"].lower()

        if book_data["availability"] == "For Rent":
            book_data["availability"] = "rent"
        elif book_data["availability"] == "For Sale":
            book_data["availability"] = "purchase"
        else:
            book_data["availability"] = book_data["availability"].lower()

        BookRepository.edit_a_book(book_id, book_data)

        # Delete old genres, if there are

        if len(book_data["genres_to_delete"]) > 0:
            BookRepository.remove_connection_of_book_to_genres(
                book_id, book_data["genres_to_delete"]
            )

        # Link new genres to book_genre_links table, if there are

        if len(book_data["genres_to_add"]) > 0:
            BookRepository.connect_book_to_genres(book_id, book_data["genres_to_add"])

        # Remove old images from Supabase book_images bucket

        supabase: Client = create_client(
            current_app.config.get("SUPABASE_URL"),
            current_app.config.get("SUPABASE_SERVICE_KEY"),
        )

        bucket_name = "book_images"

        has_deleted_an_image = False

        if len(book_data["existing_book_image_urls_to_delete"]) > 0:

            supabase.storage.from_(bucket_name).remove(
                [
                    existing_book_image_url_to_delete.split("/").pop()
                    for existing_book_image_url_to_delete in book_data[
                        "existing_book_image_urls_to_delete"
                    ]
                ]
            )

            # Remove rows of old images in book_images table

            BookRepository.remove_book_images_from_database(
                book_id, book_data["existing_book_image_urls_to_delete"]
            )

            has_deleted_an_image = True

        # Rename already uploaded images based on all_book_order

        if len(book_data["all_book_order"]) > 0 or has_deleted_an_image:
            SUPABASE_BUCKET_URL = f"{current_app.config.get("SUPABASE_URL")}/storage/v1/object/public/book_images/"

            renamed_mappings = []

            # Move files to a temporary file name first, to avoid conflicts
            temp_paths = []
            for index, file_or_url in enumerate(book_data["all_book_order"], start=1):
                if not file_or_url.startswith(SUPABASE_BUCKET_URL):
                    continue

                src_path = file_or_url.replace(SUPABASE_BUCKET_URL, "")
                final_path = f"{book_id}-{index}"

                if src_path == final_path:
                    continue

                temp_path = f"temp-{final_path}"

                supabase.storage.from_(bucket_name).move(src_path, temp_path)

                temp_paths.append((file_or_url, temp_path))

            # Move to final path
            for index, (old_url, temp_path) in enumerate(temp_paths, start=1):
                final_path = temp_path.replace("temp-", "")

                supabase.storage.from_(bucket_name).move(temp_path, final_path)

                new_url = supabase.storage.from_(bucket_name).get_public_url(final_path)
                renamed_mappings.append((old_url, new_url))

            # Update image_urls in db

            # Add a temporary value first to avoid conflicts
            temp_mappings = []
            for old_url, new_url in renamed_mappings:
                temp_url = new_url + "?temp"

                order_num = int(new_url.split(f"{book_id}-")[-1])
                temp_order_num = order_num + 1000

                BookRepository.edit_book_image_url_in_database(
                    book_id, old_url, temp_url, temp_order_num
                )
                temp_mappings.append((temp_url, new_url))

            # Change to final value afterwards
            for temp_url, final_url in temp_mappings:
                order_num = int(final_url.split(f"{book_id}-")[-1])

                BookRepository.edit_book_image_url_in_database(
                    book_id, temp_url, final_url, order_num
                )

        parsed_book_images = book_images.getlist("bookImages")

        uploaded_urls = upload_images_to_bucket(
            supabase,
            parsed_book_images,
            book_id,
            bucket_name,
            "edit",
            book_data["all_book_order"],
            book_data["existing_book_image_urls"],
        )

        # Link to new images to book_images table

        if len(uploaded_urls) > 0:
            BookRepository.add_book_images_to_database(book_id, uploaded_urls)

    @staticmethod
    def delete_a_book_service(book_id) -> None:
        """Add a new book (improve later)"""

        BookRepository.delete_all_book_genre_links_from_book(book_id)

        image_urls_dict = BookRepository.get_book_images(book_id)

        image_urls_to_delete = [
            image_url_dict["image_url"] for image_url_dict in image_urls_dict
        ]

        supabase: Client = create_client(
            current_app.config.get("SUPABASE_URL"),
            current_app.config.get("SUPABASE_SERVICE_KEY"),
        )

        bucket_name = "book_images"

        supabase.storage.from_(bucket_name).remove(
            [
                image_url_to_delete.split("/").pop()
                for image_url_to_delete in image_urls_to_delete
            ]
        )

        BookRepository.remove_book_images_from_database(book_id, image_urls_to_delete)

        has_rent_and_purchase_history = (
            BookRepository.check_if_book_has_rent_or_purchase_history(book_id)
        )

        print(f"has_rent_and_purchase_history: {has_rent_and_purchase_history}")

        if has_rent_and_purchase_history:
            BookRepository.soft_delete_a_book(book_id)
        else:
            BookRepository.delete_a_book(book_id)
