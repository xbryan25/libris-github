import type { Book } from "~/types"

export function useBooksForBookList(options?: {
                                booksPerPage?: number, 
                                pageNumber?: number, 
                                searchValue?: string, 
                                bookGenre?: string,
                                bookAvailability: string,
                            }){

  const { $apiFetch } = useNuxtApp();                            

  return $apiFetch<Book[]>(`/api/books/book-list-books`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};