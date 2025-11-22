export function useReservedAmount(){
    const { $apiFetch } = useNuxtApp();   
  
    return $apiFetch<{reservedAmount: number}>(`/api/wallets/get-reserved-amount`, {
      method: 'GET',
      credentials: 'include',
    });
  };
  