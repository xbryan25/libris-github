import type { Notification } from "~/types";

export function useRecentNotifications(numOfNotifications: number){

  const { $apiFetch } = useNuxtApp();                            

  return $apiFetch<Notification[]>(`/api/notifications/get-recent-notifications`, {
    method: 'GET',
    credentials: 'include',
    query: {
      numOfNotifications
    },
  });
};