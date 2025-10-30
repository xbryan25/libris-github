
export function useLibraryDetails(userId: string) {
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<{booksBought: number, 
                    booksOwned: number, 
                    booksRented: number}>(`/api/users/library-details/${userId}`, {
        method: 'GET',
        credentials: 'include',
    });
}