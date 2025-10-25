export function useBookGenres(){
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<string[]>(`${apiUrl}/api/books/book-genres`, {
    method: 'GET',
    credentials: 'include',
  });
};