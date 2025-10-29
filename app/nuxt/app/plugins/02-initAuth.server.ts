
import { useAuthStore } from '~/stores/useAuthStore'
import { useRefreshAccessToken, useCurrentUser } from '#imports'

export default defineNuxtPlugin(async (nuxtApp) => {
  const auth = useAuthStore()
  const isServer = import.meta.server
  if (!isServer) return 

  try {
    const event = nuxtApp.ssrContext?.event
    const cookie = event?.node?.req?.headers.cookie

    if (!cookie) {
      auth.username = null
      auth.isAuthenticated = false
      return
    }
    
    await useRefreshAccessToken('server', cookie)

    const response = await useCurrentUser('server', cookie)
    auth.username = response.username
    auth.isAuthenticated = true

  } catch {
    auth.username = null
    auth.isAuthenticated = false
  }
})