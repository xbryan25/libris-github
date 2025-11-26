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

  return {
    loading,
    error,
    approveRental,
    rejectRental,
  }
}