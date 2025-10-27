type RefreshAccessTokenResponse = {
    accessTokenExpiresAt: number
}

export function useRefreshAccessToken(runType: string, cookie? ){
    const { $apiFetch } = useNuxtApp();   

    // If loadType === 'server', it is run during SSR
    // else, run during client

    if (runType == 'client'){
        return $apiFetch<RefreshAccessTokenResponse>(`/api/users/refresh`, {
            method: 'POST',
            credentials: 'include',
        });
    } else{
        return $apiFetch<RefreshAccessTokenResponse>(`/api/users/refresh`, {
            method: 'POST',
            headers: { cookie },
        })
    }
};