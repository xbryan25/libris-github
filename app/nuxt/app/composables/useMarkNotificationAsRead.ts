

export function useMarkNotificationAsRead(notificationId: string){

  const { $apiFetch } = useNuxtApp();                            

  return $apiFetch<{message: string}>(`/api/notifications/${notificationId}/mark-as-read`, {
    method: 'PATCH',
    credentials: 'include',
  });
};