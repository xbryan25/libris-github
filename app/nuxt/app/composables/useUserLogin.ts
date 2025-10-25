type UserLoginResponse = {
    messageTitle: string
    message: string
    username: string
    user_id: string
    accessTokenExpiresAt: number
}

export function useUserLogin(emailAddress: string, password: string){
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<UserLoginResponse>(`${apiUrl}/api/users/login`, {
    method: 'POST',
    credentials: 'include',
    body: {
      emailAddress,
      password
    },
  });
};