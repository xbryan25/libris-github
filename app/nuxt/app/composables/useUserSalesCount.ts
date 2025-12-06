import { ref } from 'vue'


const API_URL = import.meta.env.VITE_API_URL

export const useUserSalesCount = () => {
  // const salesCount = ref<number>(0)
  const completedSalesCount = ref<number>(0)
  const loading = ref(true)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const fetchUserCompletedSalesCount = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<{count: number}>(`${API_URL}/api/purchases/my-completed-sales-count`, {
        credentials: 'include'
      })
      completedSalesCount.value = res.count

    } catch (e: any) {
      completedSalesCount.value = 0
      console.log('No sales found or error fetching sales count:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    completedSalesCount,
    loading,
    error,
    fetchUserCompletedSalesCount
  }
}