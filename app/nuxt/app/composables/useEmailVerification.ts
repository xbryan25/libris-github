export const useSendVerificationEmail = async (userId: string) => {
  const config = useRuntimeConfig()

  console.log('[useEmailVerification] Sending verification email for user:', userId)
  
  const response = await $fetch(`${config.public.apiBaseUrl}/api/users/send-verification-email`, {
    method: 'POST',
    credentials: 'include',
    body: {
      userId,
    },
  })

  console.log('[useEmailVerification] Send verification response:', response)
  return response
}

export const useVerifyEmailCode = async (userId: string, code: string) => {
  const config = useRuntimeConfig()

  console.log('[useEmailVerification] Verifying email code for user:', userId, 'code:', code)
  
  const response = await $fetch(`${config.public.apiBaseUrl}/api/users/verify-email`, {
    method: 'POST',
    credentials: 'include',
    body: {
      userId,
      code,
    },
  })

  console.log('[useEmailVerification] Verify email response:', response)
  return response
}

export const useResendVerificationCode = async (userId: string) => {
  const config = useRuntimeConfig()

  console.log('[useEmailVerification] Resending verification code for user:', userId)
  
  const response = await $fetch(`${config.public.apiBaseUrl}/api/users/resend-verification-code`, {
    method: 'POST',
    credentials: 'include',
    body: {
      userId,
    },
  })

  console.log('[useEmailVerification] Resend verification response:', response)
  return response
}