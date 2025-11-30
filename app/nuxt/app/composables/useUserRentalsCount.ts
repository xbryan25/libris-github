import { ref } from 'vue'


const API_URL = import.meta.env.VITE_API_URL

export const useUserRentalsCount = () => {
  // const rentalsCount = ref<number>(0)
  const completedRentalsCount = ref<number>(0)
  const loading = ref(true)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const fetchUserCompletedRentalsCount = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<{count: number}>(`${API_URL}/api/rentals/my-completed-rentals-count`, {
        credentials: 'include'
      })
      completedRentalsCount.value = res.count
    } catch (e: any) {
      completedRentalsCount.value = 0
      console.log('No rentals found or error fetching rental count:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    fetchUserCompletedRentalsCount
  }
}