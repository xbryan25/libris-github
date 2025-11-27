import { ref } from 'vue'

const API_URL = import.meta.env.VITE_API_URL

export const useRentalActions = () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const approveRental = async (
    rentalId: string,
    meetupTime: string
  ): Promise<{ success: boolean; error?: string }> => {
    loading.value = true
    error.value = null

    console.log('Approving rental:', { rentalId, meetupTime })
    console.log('API URL:', `${API_URL}/api/rentals/${rentalId}/approve`)

    try {
      const response = await $apiFetch(`${API_URL}/api/rentals/${rentalId}/approve`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          meetupTime,
        }),
      })

      console.log('Approval response:', response)
      return { success: true }
    } catch (e: any) {
      console.error('Error approving rental:', e)
      console.error('Error details:', {
        data: e.data,
        status: e.status,
        statusText: e.statusText,
        message: e.message
      })
      
      let errorMessage = 'Failed to approve rental'
      
      if (e.data?.error) {
        errorMessage = e.data.error
      } else if (e.message) {
        errorMessage = e.message
      } else if (e.statusText) {
        errorMessage = `Request failed: ${e.statusText}`
      }
      
      error.value = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const rejectRental = async (
    rentalId: string,
    reason: string
  ): Promise<{ success: boolean; error?: string }> => {
    loading.value = true
    error.value = null

    console.log('Rejecting rental:', { rentalId, reason })
    console.log('API URL:', `${API_URL}/api/rentals/${rentalId}/reject`)

    try {
      const response = await $apiFetch(`${API_URL}/api/rentals/${rentalId}/reject`, {
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
      console.error('Error rejecting rental:', e)
      console.error('Error details:', {
        data: e.data,
        status: e.status,
        statusText: e.statusText,
        message: e.message
      })
      
      let errorMessage = 'Failed to reject rental'
      
      if (e.data?.error) {
        errorMessage = e.data.error
      } else if (e.message) {
        errorMessage = e.message
      } else if (e.statusText) {
        errorMessage = `Request failed: ${e.statusText}`
      }
      
      error.value = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const cancelRental = async (
    rentalId: string
  ): Promise<{ success: boolean; error?: string }> => {
    loading.value = true
    error.value = null

    console.log('Cancelling rental:', { rentalId })
    console.log('API URL:', `${API_URL}/api/rentals/${rentalId}/cancel`)

    try {
      const response = await $apiFetch(`${API_URL}/api/rentals/${rentalId}/cancel`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      console.log('Cancel response:', response)
      return { success: true }
    } catch (e: any) {
      console.error('Error cancelling rental:', e)
      console.error('Error details:', {
        data: e.data,
        status: e.status,
        statusText: e.statusText,
        message: e.message
      })
      
      let errorMessage = 'Failed to cancel rental'
      
      if (e.data?.error) {
        errorMessage = e.data.error
      } else if (e.message) {
        errorMessage = e.message
      } else if (e.statusText) {
        errorMessage = `Request failed: ${e.statusText}`
      }
      
      error.value = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const confirmPickup = async (
    rentalId: string
  ): Promise<{ success: boolean; error?: string; data?: any }> => {
    loading.value = true
    error.value = null

    console.log('Confirming pickup:', { rentalId })

    try {
      const response = await $apiFetch(`${API_URL}/api/rentals/${rentalId}/confirm-pickup`, {
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
      
      if (e.data?.error) {
        errorMessage = e.data.error
      } else if (e.message) {
        errorMessage = e.message
      }
      
      error.value = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const confirmReturn = async (
    rentalId: string
  ): Promise<{ success: boolean; error?: string; data?: any }> => {
    loading.value = true
    error.value = null

    console.log('Confirming return:', { rentalId })

    try {
      const response = await $apiFetch(`${API_URL}/api/rentals/${rentalId}/confirm-return`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      console.log('Confirm return response:', response)
      return { success: true, data: response}
    } catch (e: any) {
      console.error('Error confirming return:', e)
      
      let errorMessage = 'Failed to confirm return'
      
      if (e.data?.error) {
        errorMessage = e.data.error
      } else if (e.message) {
        errorMessage = e.message
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
    approveRental,
    rejectRental,
    cancelRental,
    confirmPickup,
    confirmReturn
  }
}