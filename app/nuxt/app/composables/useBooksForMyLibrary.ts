import type { MyLibraryBook } from "~/types"

export function useBooksForMyLibrary(options?: {
                                booksPerPage?: number, 
                                pageNumber?: number, 
                                searchValue?: string, 
                                bookGenre?: string,
                                bookAvailability: string,
                            }){

  const { $apiFetch } = useNuxtApp();                            

  return $apiFetch<MyLibraryBook[]>(`/api/books/my-library-books`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};