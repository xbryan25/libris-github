import { ref } from 'vue'

type DashboardSummary = {
  books_borrowed: number
  currently_lending: number
  currently_renting: number
  books_sold: number
  books_bought: number
  total_earnings: number
}

export const useDashboard = () => {

  const { $apiFetch } = useNuxtApp();   

  const summary = ref<DashboardSummary>({
    books_borrowed: 0,
    currently_lending: 0,
    currently_renting: 0,
    books_sold: 0,
    books_bought: 0,
    total_earnings: 0,
  })
  const loading = ref(true)
  const username = ref<string | null>(null)
  const error = ref<string | null>(null)

  const fetchSummary = async () => {
    loading.value = true
    error.value = null

    try {
      const res = await $apiFetch<DashboardSummary>(`/api/dashboard/summary`, {
        credentials: 'include'
      })
      summary.value = res
    } catch (e: any) {
      error.value = e?.message || 'Failed to fetch dashboard summary'
    } finally {
      loading.value = false
    }
  }

  const fetchUsername = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<{ username: string }>(`/api/users/me`, {
        credentials: 'include' 
      })
      username.value = res.username
    } catch (e: any) {
      error.value = e?.message || 'Failed to fetch username'
    } finally {
      loading.value = false
    }
  }

  const fetchAll = async () => {
    await Promise.all([fetchSummary(), fetchUsername()])
  }

  return { summary, username, loading, error, fetchAll }
}
