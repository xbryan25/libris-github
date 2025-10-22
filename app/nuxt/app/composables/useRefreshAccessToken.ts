type RefreshAccessTokenResponse = {
    accessTokenExpiresAt: number
}

export function useRefreshAccessToken(runType: string, cookie? ){
    const apiUrl = import.meta.env.VITE_API_URL;

    // If loadType === 'server', it is run during SSR
    // else, run during client

    if (runType == 'client'){
        return $fetch<RefreshAccessTokenResponse>(`${apiUrl}/api/users/refresh`, {
            method: 'POST',
            credentials: 'include',
        });
    } else{
        return $fetch<RefreshAccessTokenResponse>(`${apiUrl}/api/users/refresh`, {
            method: 'POST',
            headers: { cookie },
        })
    }
};