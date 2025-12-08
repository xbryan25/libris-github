import type { Notification } from "~/types";

export function useNotifications(options?: {
                                booksPerPage?: number, 
                                pageNumber?: number, 
                                readStatus?: string, 
                                order?: string
                            }){

  const { $apiFetch } = useNuxtApp();                            

  return $apiFetch<Notification[]>(`/api/notifications`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};