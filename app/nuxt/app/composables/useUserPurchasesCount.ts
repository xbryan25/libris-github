import { ref } from 'vue'


const API_URL = import.meta.env.VITE_API_URL

export const useUserPurchasesCount = () => {
  // const purchasesCount = ref<number>(0)
  const completedPurchasesCount = ref<number>(0)
  const loading = ref(true)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const fetchUserCompletedPurchasesCount = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<{count: number}>(`${API_URL}/api/purchases/my-completed-purchases-count`, {
        credentials: 'include'
      })
      completedPurchasesCount.value = res.count

    } catch (e: any) {
      completedPurchasesCount.value = 0
      console.log('No purchases found or error fetching purchase count:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    completedPurchasesCount,
    loading,
    error,
    fetchUserCompletedPurchasesCount
  }
}