import type { Book } from "~/types"

export function useBooksForBookList(options?: {
                                booksPerPage?: number, 
                                pageNumber?: number, 
                                searchValue?: string, 
                                bookGenre?: string,
                                bookAvailability: string,
                            }){

  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<Book[]>(`${apiUrl}/api/books/book-list-books`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};