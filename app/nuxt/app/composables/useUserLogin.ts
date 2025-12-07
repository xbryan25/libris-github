type UserLoginResponse = {
    messageTitle: string
    message: string
    username: string
    userId: string
    isEmailVerified: boolean
}


export function useUserLogin(emailAddress: string, password: string){
  const baseURL = import.meta.env.VITE_API_URL;

  return $fetch<UserLoginResponse>(`${baseURL}/api/users/login`, {
    method: 'POST',
    credentials: 'include',
    body: {
      emailAddress,
      password
    },
  });
};