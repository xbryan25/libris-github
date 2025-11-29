type UserGoogleLoginResponse = {
    messageTitle: string
    message: string
    username: string
    user_id: string
    accessTokenExpiresAt: number
}

export function useUserGoogleLogin(code: string){
  const baseURL = import.meta.env.VITE_API_URL;

  return $fetch<UserGoogleLoginResponse>(`${baseURL}/api/users/google-login`, {
    method: 'POST',
    credentials: 'include',
    body: {
      code
    },
  });
};