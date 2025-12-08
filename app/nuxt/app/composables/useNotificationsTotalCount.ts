

export function useNotificationsTotalCount(readStatus: string){

  const { $apiFetch } = useNuxtApp();                            

  return $apiFetch<{totalCount: number}>(`/api/notifications/total-count`, {
    method: 'GET',
    credentials: 'include',
    query: {
      readStatus
    },
  });
};