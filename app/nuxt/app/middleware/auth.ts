
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

    } catch {
        auth.username = null
        auth.isAuthenticated = false

        if (to.path !== '/login') return navigateTo('/login')
    }
})