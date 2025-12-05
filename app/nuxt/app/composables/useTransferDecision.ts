import { ref } from 'vue'

const API_URL = import.meta.env.VITE_API_URL

export const useTransferDecision = () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const submitTransferDecision = async (
    purchaseId: string,
    transferOwnership: boolean
  ): Promise<{ success: boolean; error?: string }> => {
    loading.value = true
    error.value = null

    try {
      await $apiFetch(`${API_URL}/api/purchases/${purchaseId}/transfer-decision`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          transfer_ownership: transferOwnership,
        }),
      })

      return { success: true }
    } catch (e: any) {
      console.error('Error submitting transfer decision:', e)
      
      let errorMessage = 'Failed to submit transfer decision'
      
      if (e?.error) {
        errorMessage = e.error
      } else if (e?.message) {
        errorMessage = e.message
      } else if (typeof e === 'string') {
        errorMessage = e
      }
      
      error.value = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    submitTransferDecision,
  }
}