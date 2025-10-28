
import { useAuthStore } from '~/stores/useAuthStore'
import { useRefreshAccessToken, useCurrentUser } from '#imports'

export default defineNuxtRouteMiddleware(async (to) => {
    const auth = useAuthStore()
    const now = Date.now()

    // Determine context, if on server or client
    const isServer = import.meta.server
    const runType = isServer ? 'server' : 'client'

    let cookie: string | undefined
    
    if (isServer) {
        const event = useRequestEvent()
        cookie = event?.node?.req?.headers.cookie
    }

    // If no cookie on server, redirect
    if (isServer && !cookie) {
        if (to.path !== '/login') return navigateTo('/login')
        return
    }

    try {
        const now = Date.now()

        try {
            // Check if access_token_cookie currently exists in the browser
            const response = await useCurrentUser(runType, cookie)
            auth.username = response.username
            auth.isAuthenticated = true
            auth.user_id = response.user_id

        } catch {
            // If access_token_cookie does not exist, refresh access_token_cookie
            const data = await useRefreshAccessToken(runType, cookie)
            auth.accessTokenExpiresAt = data?.accessTokenExpiresAt

            const retryResponse = await useCurrentUser(runType, cookie)
            auth.username = retryResponse.username
            auth.isAuthenticated = true
        }
        
        // If accessTokenExpiresAt in Pinia doesn't exist or expires in 30 seconds, refresh access_token_cookie
        if (!auth.accessTokenExpiresAt || now > auth.accessTokenExpiresAt - 30_000) {
            const data = await useRefreshAccessToken(runType, cookie)
            auth.accessTokenExpiresAt = data?.accessTokenExpiresAt
        }

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
        auth.accessTokenExpiresAt = null

        if (to.path !== '/login') return navigateTo('/login')
    }
})