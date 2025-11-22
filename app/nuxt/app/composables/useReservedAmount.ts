export function useReservedAmount(){
    const { $apiFetch } = useNuxtApp();   
  
    return $apiFetch<{reserved_amount: number}>(`/api/wallets/get-reserved-amount`, {
      method: 'GET',
      credentials: 'include',
    });
  };
  