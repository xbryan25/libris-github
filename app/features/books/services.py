from .repository import BookRepository

from app.common.dataclasses import Book

from app.utils.converters import convert_book_dict


class BookServices:

    @staticmethod
    def get_many_books_service(params) -> list[Book]:
        """
        Retrieve details of different books based on pagination, optional search, genre, and availability filters.

        Args:
            params (dict): A dictionary containing the pagination details,  optional search, genre, and availability filters.
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

        books = BookRepository.get_many_books(params)

        book_dataclasses = []

        for book in books:
            # Convert dict to dataclass before appending
            book_dataclasses.append(convert_book_dict(book))

        return book_dataclasses
