type CurrentUserResponse = {
    username: string
	userId: string
	isEmailVerified: boolean
}

export function useCurrentUser() {
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<CurrentUserResponse>(`/api/users/me`, {
			method: 'GET',
			credentials: 'include',
	});
}