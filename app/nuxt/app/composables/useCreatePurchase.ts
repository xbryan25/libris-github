import { ref } from 'vue'

const API_URL = import.meta.env.VITE_API_URL

export const useCreatePurchase = () => {
  const purchaseExists = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const toast = useToast()

  const { $apiFetch } = useNuxtApp()

  const checkPurchaseExists = async (bookId: string) => {
    try {
      const res = await $apiFetch<{ exists: boolean }>(
        `${API_URL}/api/purchases/check/${bookId}`,
        { method: 'GET', credentials: 'include' }
      )
      purchaseExists.value = res.exists
    } catch (e: any) {
      console.error(e)
    }
  }

  const createPurchase = async (payload: {
    book_id: string
    total_buy_cost: number
    meetup_location: string
    meetup_date: string
    meetup_time_window: string
  }) => {
    loading.value = true
    error.value = null

    try {
      const res = await $apiFetch(`${API_URL}/api/purchases/create`, {
        method: 'POST',
        body: payload,
        credentials: 'include'
      })
      toast.add({
        title: 'Success',
        description: 'Purchase created successfully',
        color: 'success',
      })
      return res
    } catch (err: any) {
      error.value = err?.data?.error || err?.message || 'Failed to create purchase'
      toast.add({
        title: 'Error',
        description: error.value ?? 'Failed to create purchase',
        color: 'error',
      })
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    createPurchase,
    checkPurchaseExists,
    purchaseExists
  }
}
