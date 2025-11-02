export function useTotalCountForMyLibrary(options?: {
        searchValue?: string, 
        bookGenre?: string,
        bookAvailability: string,
    }){

  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<{totalCount: number}>(`/api/books/my-library-books-count`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};