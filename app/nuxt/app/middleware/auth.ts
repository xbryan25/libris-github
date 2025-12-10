
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
        

        if (response.authProvider === 'google') {
            auth.isGoogleLogin = true
        }

        if (to.params.id) {
            if (to.params.id === auth.userId) {
                return navigateTo('/users/me')
            }
        }

        if (!auth.isEmailVerified) {
            return navigateTo(`/verify-email?userId=${auth.userId}`);
        }

        if (to.path.includes('/change-password-code')) {
            if (!auth.allowedInputChangePasswordCode) {
                return navigateTo('/users/me')
            }

            auth.allowedInputChangePasswordCode = false
        }

        if (to.path.includes('/change-password-new')) {
            if (!auth.allowedChangePassword) {
                return navigateTo('/users/me')
            }

            auth.allowedChangePassword = false
        }


    } catch {
        auth.username = null
        auth.userId = null
        auth.isAuthenticated = false
        auth.isEmailVerified = false
        auth.isGoogleLogin = false;

        if (to.path !== '/login') return navigateTo('/login')
    }
})