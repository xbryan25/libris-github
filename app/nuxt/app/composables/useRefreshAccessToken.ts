type RefreshAccessTokenResponse = {
    accessTokenExpiresAt: number
}

export function useRefreshAccessToken(){
    const { $apiFetch } = useNuxtApp();   
    
    return $apiFetch<RefreshAccessTokenResponse>(`/api/users/refresh`, {
        method: 'POST',
        credentials: 'include',
    });
};