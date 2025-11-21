

export function useMarkMultipleNotificationAsRead(notificationIds: Set<string>){

  const { $apiFetch } = useNuxtApp();
  
  console.log(notificationIds)

  return $apiFetch<{message: string}>(`/api/notifications/mark-as-read`, {
    method: 'PATCH',
    credentials: 'include',
    body: { notificationIds: Array.from(notificationIds) }
  });
};