export const useUserSignup = async (username: string, emailAddress: string, password: string) => {
  const baseURL = import.meta.env.VITE_API_URL;
  
  return $fetch(`${baseURL}/api/users/signup`, {
    method: 'POST',
    credentials: 'include',
    body: {
      username,
      emailAddress,
      password,
    },
  })

}