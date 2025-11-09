type CurrentUserResponse = {
    username: string
	user_id: string
}

export function useCurrentUser() {
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<CurrentUserResponse>(`/api/users/me`, {
			method: 'GET',
			credentials: 'include',
	});
}