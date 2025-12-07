
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
        auth.userId = response.userId
        auth.isAuthenticated = true
        auth.isEmailVerified = response.isEmailVerified

        console.log("================= " + auth.isEmailVerified)

        // --- Redirect if user navigates to their own ID ---
        if (to.params.id) {
            if (to.params.id === auth.userId) {
                console.log('Redirecting to /users/me')
                return navigateTo('/users/me')
            } else {
                console.log('Viewing another user profile:', to.params.id)
            }
        }

        if (!auth.isEmailVerified) {
            console.log('reach here?')
            return navigateTo(`/verify-email?userId=${auth.userId}`);
        }

    } catch {
        auth.username = null
        auth.userId = null
        auth.isAuthenticated = false
        auth.isEmailVerified = false

        if (to.path !== '/login') return navigateTo('/login')
    }
})