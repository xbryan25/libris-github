

export function useChangeNotificationsReadStatus(notificationIds: Set<string>, isReadChange: boolean){

  const { $apiFetch } = useNuxtApp();
  
  console.log(notificationIds)

  return $apiFetch<{message: string}>(`/api/notifications/change-read-status`, {
    method: 'PATCH',
    credentials: 'include',
    body: { notificationIds: Array.from(notificationIds), isReadChange }
  });
};