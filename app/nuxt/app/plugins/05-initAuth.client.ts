import { useAuthStore } from '~/stores/useAuthStore'

export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()

  try {
    const response = await useCurrentUser('client')
    auth.username = response.username
    auth.isAuthenticated = true
  } catch {
    auth.username = null
    auth.isAuthenticated = false
  }
})