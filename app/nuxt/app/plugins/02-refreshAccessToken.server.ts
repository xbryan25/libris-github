import { useAuthStore } from '~/stores/useAuthStore'
import { useRefreshAccessToken } from '#imports'

export default defineNuxtPlugin(async (nuxtApp) => {
  const auth = useAuthStore()

  try {
    const event = nuxtApp.ssrContext?.event
    const cookie = event?.node?.req?.headers.cookie

    if (!cookie) return

    const data = await useRefreshAccessToken('server', cookie)
    
    if (data && data.accessTokenExpiresAt) {
      auth.accessTokenExpiresAt = data.accessTokenExpiresAt
    }
  } catch {
    // Proceed silently if token refresh fails (unauthenticated SSR)
  }
})