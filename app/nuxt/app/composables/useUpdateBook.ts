
export function useUpdateBook(bookId: string, bookFormData: FormData){
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<{ message: string }>(`/api/books/${bookId}`, {
    method: 'PATCH',
    credentials: 'include',
    body: bookFormData
  });
};