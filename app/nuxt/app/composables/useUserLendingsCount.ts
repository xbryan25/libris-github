import { ref } from 'vue'


const API_URL = import.meta.env.VITE_API_URL

export const useUserLendingsCount = () => {
  // const rentalsCount = ref<number>(0)
  const completedLendingsCount = ref<number>(0)
  const loading = ref(true)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const fetchUserCompletedLendingsCount = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<{count: number}>(`${API_URL}/api/rentals/my-completed-lendings-count`, {
        credentials: 'include'
      })
      completedLendingsCount.value = res.count

      console.log('lend counttt ' + completedLendingsCount.value)
    } catch (e: any) {
      completedLendingsCount.value = 0
      console.log('No lendings found or error fetching lending count:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    completedLendingsCount,
    loading,
    error,
    fetchUserCompletedLendingsCount
  }
}