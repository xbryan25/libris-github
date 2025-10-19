type CurrentUserResponse = {
    username: string
}

export function useCurrentUser(loadType: string, cookie?) {
  const apiUrl = import.meta.env.VITE_API_URL;

  // If loadType === 'server', it is run during SSR
  // else, run during client

  if (loadType == 'client'){
		return $fetch<CurrentUserResponse>(`${apiUrl}/api/users/me`, {
			method: 'GET',
			credentials: 'include',
		});
	} else{
		return $fetch<CurrentUserResponse>(`${apiUrl}/api/users/me`, {
			method: 'GET',
			headers: { cookie },
		})
	}
}