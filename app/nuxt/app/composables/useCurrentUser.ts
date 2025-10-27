type CurrentUserResponse = {
    username: string
}

export function useCurrentUser(loadType: string, cookie?) {
  const { $apiFetch } = useNuxtApp();   

  // If loadType === 'server', it is run during SSR
  // else, run during client

  if (loadType == 'client'){
		return $apiFetch<CurrentUserResponse>(`/api/users/me`, {
			method: 'GET',
			credentials: 'include',
		});
	} else{
		return $apiFetch<CurrentUserResponse>(`/api/users/me`, {
			method: 'GET',
			headers: { cookie },
		})
	}
}