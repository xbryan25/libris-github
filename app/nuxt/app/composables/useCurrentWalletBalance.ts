
export function useCurrentWalletBalance(){
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<{currentWalletBalance: number}>(`/api/wallets/get-current-balance`, {
    method: 'GET',
    credentials: 'include',
  });
};
