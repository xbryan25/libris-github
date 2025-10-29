
import { useAuthStore } from '~/stores/useAuthStore'

// Works client-only

export default defineNuxtRouteMiddleware(async (to) => {
    const auth = useAuthStore()

    // Determine context, if on server or client
    const isServer = import.meta.server

    if (isServer) {
        const event = useRequestEvent();
        const cookie = event?.node?.req?.headers.cookie;

        // If no cookies at all → definitely unauthenticated
        if (!cookie) {
            return navigateTo('/login', { redirectCode: 302 });
        }

        // ✅ stop here, don’t continue to client-specific logic
        return;
    }

    try {
        // // Wait 10 seconds to refresh token again, if access token is removed while still in cooldown, redirect to login
        await safeRefresh('client')
        // await useRefreshAccessToken('client')
        const response = await useCurrentUser('client')
        auth.username = response.username
        auth.isAuthenticated = true

         // --- Debug logging ---
        const logPrefix = isServer ? '[SSR]' : '[Client]'
        console.log(logPrefix, 'Route path:', to.path)
        console.log(logPrefix, 'Route params:', to.params)
        console.log(logPrefix, 'Logged-in user_id:', auth.user_id)

        // --- Redirect if user navigates to their own ID ---
        if (to.params.id) {
            if (to.params.id === auth.user_id) {
                console.log(logPrefix, 'Redirecting to /users/me')
                return navigateTo('/users/me')
            } else {
                console.log(logPrefix, 'Viewing another user profile:', to.params.id)
            }
        }

    } catch {
        auth.username = null
        auth.isAuthenticated = false

        if (to.path !== '/login') return navigateTo('/login')
    }
})