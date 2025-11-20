
export function useBuyReadits(selectedPack: string){
  const { $apiFetch } = useNuxtApp();   

  return $apiFetch<{invoiceUrl: string}>(`/api/wallets/buy-readits`, {
    method: 'POST',
    credentials: 'include',
    body: { selectedPack }
  });
};
