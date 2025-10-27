
export function useTotalBookCountForBookList(options?: {
                                searchValue?: string, 
                                bookGenre?: string,
                                bookAvailability: string,
                            }){

  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<{totalCount: number}>(`${apiUrl}/api/books/book-list-books-count`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};