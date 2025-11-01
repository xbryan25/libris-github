export const useUserSignup = async (username: string, emailAddress: string, password: string) => {
  const apiURL = import.meta.env.VITE_API_URL;
  
  return $fetch(`${apiURL}/api/users/signup`, {
    method: 'POST',
    credentials: 'include',
    body: {
      username,
      emailAddress,
      password,
    },
  })

}