export const useSendVerificationEmail = async (userId: string) => {
  const { $apiFetch } = useNuxtApp();   
  
  const response = await $apiFetch(`/api/users/send-verification-email`, {
    method: 'POST',
    credentials: 'include',
    body: {
      userId,
    },
  })

  console.log('send email')
  return response
}

export const useVerifyEmailCode = async (userId: string, code: string) => {
  const { $apiFetch } = useNuxtApp(); 
  
  const response = await $apiFetch(`/api/users/verify-email`, {
    method: 'POST',
    credentials: 'include',
    body: {
      userId,
      code,
    },
  })

  return response
}

export const useResendVerificationCode = async (userId: string) => {
  const { $apiFetch } = useNuxtApp(); 

  const response = await $apiFetch(`/api/users/resend-verification-code`, {
    method: 'POST',
    credentials: 'include',
    body: {
      userId,
    },
  })

  return response
}