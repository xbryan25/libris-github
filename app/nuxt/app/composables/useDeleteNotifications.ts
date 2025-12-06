

export function useDeleteNotifications(notificationIds: Set<string>){

  const { $apiFetch } = useNuxtApp();

  return $apiFetch<{message: string}>(`/api/notifications/delete`, {
    method: 'DELETE',
    credentials: 'include',
    body: { notificationIds: Array.from(notificationIds) }
  });
};