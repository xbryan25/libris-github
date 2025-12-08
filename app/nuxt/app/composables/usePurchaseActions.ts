import { ref } from 'vue'

const API_URL = import.meta.env.VITE_API_URL

export const usePurchaseActions = () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const approvePurchase = async (
    purchaseId: string,
    meetupTime: string
  ): Promise<{ success: boolean; error?: string }> => {
    loading.value = true
    error.value = null

    try {
      const response = await $apiFetch(`${API_URL}/api/purchases/${purchaseId}/approve`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          meetupTime,
        }),
      })

      return { success: true }
    } catch (e: any) {
      console.error('Error approving purchase:', e)
      
      let errorMessage = 'Failed to approve purchase'
      
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

  const rejectPurchase = async (
    purchaseId: string,
    reason: string
  ): Promise<{ success: boolean; error?: string }> => {
    loading.value = true
    error.value = null

    console.log('Rejecting purchase:', { purchaseId, reason })

    try {
      const response = await $apiFetch(`${API_URL}/api/purchases/${purchaseId}/reject`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          reason,
        }),
      })

      console.log('Rejection response:', response)
      return { success: true }
    } catch (e: any) {
      console.error('Error rejecting purchase:', e)
      
      let errorMessage = 'Failed to reject purchase'
      
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

  const cancelPurchase = async (
    purchaseId: string
  ): Promise<{ success: boolean; error?: string }> => {
    loading.value = true
    error.value = null

    console.log('Cancelling purchase:', { purchaseId })

    try {
      const response = await $apiFetch(`${API_URL}/api/purchases/${purchaseId}/cancel`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      console.log('Cancel response:', response)
      return { success: true }
    } catch (e: any) {
      console.error('Error cancelling purchase:', e)
      
      let errorMessage = 'Failed to cancel purchase'
    
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

  const confirmPickup = async (
    purchaseId: string
  ): Promise<{ success: boolean; error?: string; data?: any }> => {
    loading.value = true
    error.value = null

    console.log('Confirming pickup:', { purchaseId })

    try {
      const response = await $apiFetch(`${API_URL}/api/purchases/${purchaseId}/confirm-pickup`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      console.log('Confirm pickup response:', response)
      return { success: true, data: response}
    } catch (e: any) {
      console.error('Error confirming pickup:', e)
      
      let errorMessage = 'Failed to confirm pickup'
      
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
    approvePurchase,
    rejectPurchase,
    cancelPurchase,
    confirmPickup
  }
}