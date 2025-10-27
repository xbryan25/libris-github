import { useAuthStore } from '~/stores/useAuthStore'

// This redirects users to /dashboard if already logged in

export default defineNuxtRouteMiddleware(() => {
  const auth = useAuthStore()

  if (auth.isAuthenticated) {
    console.log('rahhhhhhhhh')
    return navigateTo('/dashboard')
  }
})