import type { Book } from "~/types"

export function useBooksForBookList(options?: {
  booksPerPage?: number,
  pageNumber?: number,
  searchValue?: string,
  bookGenre?: string,
  bookAvailability: string,
  minPrice?: number | null,
  maxPrice?: number | null,
  kmRadius?: number | null,
  userLat?: number | null,
  userLng?: number | null,
}) {

  const { $apiFetch } = useNuxtApp();

  return $apiFetch<Book[]>(`/api/books/book-list-books`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};