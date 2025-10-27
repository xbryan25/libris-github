type UserLoginResponse = {
    messageTitle: string
    message: string
    username: string
    accessTokenExpiresAt: number
}

export function useUserLogin(emailAddress: string, password: string){
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<UserLoginResponse>(`/api/users/login`, {
    method: 'POST',
    credentials: 'include',
    body: {
      emailAddress,
      password
    },
  });
};