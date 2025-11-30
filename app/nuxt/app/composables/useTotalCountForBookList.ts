
export function useTotalBookCountForBookList(options?: {
  searchValue?: string,
  bookGenre?: string,
  bookAvailability: string,
  minPrice?: number | null,
  maxPrice?: number | null,
}) {

  const { $apiFetch } = useNuxtApp();

  return $apiFetch<{ totalCount: number }>(`/api/books/book-list-books-count`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};