from .repository import BookRepository

from app.common.dataclasses import Book

from app.utils.converters import convert_book_dict


class BookServices:

    @staticmethod
    def get_many_books_service(user_id, params) -> list[Book]:
        """
        Retrieve details of different books based on pagination, optional search, genre, and availability filters.

        Args:
            user_id (str): user_id of the user to prevent getting books that the current user owns.
            params (dict): A dictionary containing the pagination details, optional search, genre, and availability filters.
                Expected keys include:
                    - "books_per_page" (str): The number of book details to retrieve.
                    - "page_number" (str): This number will be multiplied by books_per_page then serve as the
                                            offset for pagination.
                    - "search_value" (str): The value to search for.
                    - "genre" (str): The genre or category of books to filter by.
                    - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".

        Returns:
            list[Book]: A list of Book dataclass instances representing books_per_page students.
        """

        books = BookRepository.get_many_books(user_id, params)

        book_dataclasses = []

        for book in books:
            # Convert dict to dataclass before appending
            book_dataclasses.append(convert_book_dict(book))

        return book_dataclasses

    @staticmethod
    def get_total_book_count_service(user_id, params) -> int:
        """
        Retrieve the total count of books based on pagination, optional search, genre, and availability filters.

        Args:
            params (dict): A dictionary containing the optional search, genre, and availability filters.
                Expected keys include:
                    - "search_value" (str): The value to search for.
                    - "genre" (str): The genre or category of books to filter by.
                    - "availability" (str): The availability status of the book — can be "For Rent", "For Sale", or "Both".

        Returns:
            int: The total book count, with search, genre, and availability filters being optionally applied.
        """

        print(BookRepository.get_total_book_count(user_id, params))

        return BookRepository.get_total_book_count(user_id, params)["count"]
