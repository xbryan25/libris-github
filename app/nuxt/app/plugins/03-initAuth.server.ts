import { useAuthStore } from '~/stores/useAuthStore'

export default defineNuxtPlugin(async (nuxtApp) => {
  const auth = useAuthStore()

  try {
    // Access incoming request (only exists on server)
    const event = nuxtApp.ssrContext?.event
    const cookie = event?.node?.req?.headers.cookie

    if (!cookie) {
      auth.username = null
      auth.isAuthenticated = false
      return
    }

    const response = await useCurrentUser('server', cookie)
    auth.username = response.username
    auth.isAuthenticated = true
  } catch {
    auth.username = null
    auth.isAuthenticated = false
  }
})