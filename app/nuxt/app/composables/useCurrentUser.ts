type CurrentUserResponse = {
    username: string
	userId: string
	isEmailVerified: boolean
	authProvider: string
}

export function useCurrentUser() {
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<CurrentUserResponse>(`/api/users/me`, {
			method: 'GET',
			credentials: 'include',
	});
}