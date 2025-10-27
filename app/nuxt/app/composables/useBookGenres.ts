export function useBookGenres(){
  const { $apiFetch } = useNuxtApp();

  return $apiFetch<string[]>(`/api/books/book-genres`, {
    method: 'GET',
    credentials: 'include',
  });
};