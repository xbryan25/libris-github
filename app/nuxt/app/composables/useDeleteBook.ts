export function useDeleteBook(bookId: string, title: string){
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<{ message: string }>(`/api/books/${bookId}`, {
    method: 'DELETE',
    credentials: 'include',
    body: {title}
  });
};