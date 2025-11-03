
export function useCreateBook(bookFormData: FormData){
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<{ message: string }>(`/api/books/`, {
    method: 'POST',
    credentials: 'include',
    body: bookFormData
  });
};