export const useUserSignup = async (username: string, emailAddress: string, password: string) => {
  const config = useRuntimeConfig()
  
  const response = await $fetch(`${config.public.apiBaseUrl}/users/signup`, {
    method: 'POST',
    credentials: 'include',
    body: {
      username,
      emailAddress,
      password,
    },
  })

  return response
}