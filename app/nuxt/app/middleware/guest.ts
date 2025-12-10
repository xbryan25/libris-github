import { useAuthStore } from '~/stores/useAuthStore'

// This redirects users to /dashboard if already logged in

export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()

  console.log('test here')

  // If not authenticated → allow access
  if (!auth.isAuthenticated) {
    if (to.path.startsWith('/verify-email')){
      return navigateTo('/login')
    } 

    return
  }

  // Authenticated & verified → redirect away from guest pages
  if (auth.isEmailVerified) {
    return navigateTo('/dashboard')
  }

  // Authenticated & NOT verified
  if (!auth.isEmailVerified) {
    // Allow access to /verify-email
    if (to.path.startsWith('/verify-email') && to.query.userId === auth.userId) return

    // User is trying to access login/signup → log them out
    await useUserLogout()

    auth.username = null;
    auth.userId = null;
    auth.isAuthenticated = false;
    auth.isEmailVerified = false;
    auth.isGoogleLogin = false;

    return navigateTo('/login')
  }
})