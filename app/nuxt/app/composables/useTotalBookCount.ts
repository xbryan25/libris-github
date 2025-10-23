type UseEntitiesResponse = {
    totalCount: number
}

export function useTotalBookCount(options?: {
                                searchValue?: string, 
                                genre?: string,
                                availability: string,
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