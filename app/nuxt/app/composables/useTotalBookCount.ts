type UseEntitiesResponse = {
    totalCount: number
}

export function useTotalBookCount(options?: {
                                searchValue?: string, 
                                bookGenre?: string,
                                bookAvailability: string,
                            }){

  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<UseEntitiesResponse>(`${apiUrl}/api/books/total-count`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};