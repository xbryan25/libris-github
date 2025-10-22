
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

    } catch {
        auth.username = null
        auth.isAuthenticated = false
        auth.accessTokenExpiresAt = null

        if (to.path !== '/login') return navigateTo('/login')
    }
})