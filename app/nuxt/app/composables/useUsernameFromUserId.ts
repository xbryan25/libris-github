type CurrentUserResponse = {
    username: string
}

export function useUsernameFromUserId(userId: string) {
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<CurrentUserResponse>(`/api/users/username/${userId}`, {
        method: 'GET',
        credentials: 'include',
    });
}