
export const useSubmitNewUsername = async (userId: string | null, username: string) => {
  const baseURL = import.meta.env.VITE_API_URL;
  
  return $fetch<{ messageTitle: string, message: string }>(`${baseURL}/api/users/new-username`, {
    method: 'POST',
    credentials: 'include',
    body: {
      userId,
      username
    },
  })
}