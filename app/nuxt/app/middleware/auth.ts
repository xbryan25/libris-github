
import { useAuthStore } from '~/stores/useAuthStore'

// Works client-only

export default defineNuxtRouteMiddleware(async (to) => {
    const auth = useAuthStore()

    try {
        // Wait 10 seconds to refresh token again, if access token is removed while still in cooldown, redirect to login
        await safeRefresh()
        // await useRefreshAccessToken()
        const response = await useCurrentUser()
        auth.username = response.username
        auth.isAuthenticated = true

        // --- Debug logging ---
        console.log('Route path:', to.path)
        console.log('Route params:', to.params)
        console.log('Logged-in user_id:', auth.user_id)

        // --- Redirect if user navigates to their own ID ---
        if (to.params.id) {
            if (to.params.id === auth.user_id) {
                console.log('Redirecting to /users/me')
                return navigateTo('/users/me')
            } else {
                console.log('Viewing another user profile:', to.params.id)
            }
        }

    } catch {
        auth.username = null
        auth.isAuthenticated = false

        if (to.path !== '/login') return navigateTo('/login')
    }
})