import { useAuthStore } from '~/stores/useAuthStore'
import { useRefreshAccessToken } from '#imports'

export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()

  try {
    const data = await useRefreshAccessToken('client')
    if (data && data.accessTokenExpiresAt) {
      auth.accessTokenExpiresAt = data.accessTokenExpiresAt
    }
  } catch {
    // Proceed to initAuth handle unauthenticated state
  }
})