
export function useCurrentWalletBalance(){

  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<{currentWalletBalance: number}>(`${apiUrl}/api/wallets/get-current-balance`, {
    method: 'GET',
    credentials: 'include',
  });
};
