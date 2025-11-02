
export function useUsernameFromUserId(userId: string) {
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<{username: string}>(`/api/users/username/${userId}`, {
        method: 'GET',
        credentials: 'include',
    });
}