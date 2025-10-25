import type { Book } from "~/types"

export function useBooks(options?: {
                                booksPerPage?: number, 
                                pageNumber?: number, 
                                searchValue?: string, 
                                bookGenre?: string,
                                bookAvailability: string,
                            }){

  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<Book[]>(`${apiUrl}/api/books/`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};