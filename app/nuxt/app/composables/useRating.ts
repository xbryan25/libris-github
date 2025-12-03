import { ref } from 'vue'

const API_URL = import.meta.env.VITE_API_URL

type RatingType = 'rental' | 'lending' | 'purchase' | 'sale'

export const useRating = () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const submitRating = async (
    transactionId: string,
    rating: number,
    review: string,
    from: RatingType
  ): Promise<{ success: boolean; error?: string }> => {
    loading.value = true
    error.value = null

    try {
      // Determine endpoint based on transaction type
      const isRental = from === 'rental' || from === 'lending'
      const endpoint = isRental 
        ? `${API_URL}/api/ratings/rental/${transactionId}/rate`
        : `${API_URL}/api/ratings/purchase/${transactionId}/rate`

      await $apiFetch(endpoint, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rating,
          review,
          from,
        }),
      })

      return { success: true }
    } catch (e: any) {
      console.error('Error submitting rating:', e)
      
      let errorMessage = 'Failed to submit rating'
      
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

  const getUserRatings = async (
    userId: string
  ): Promise<{ success: boolean; ratings?: any[]; error?: string }> => {
    loading.value = true
    error.value = null

    try {
      const response = await $apiFetch(`${API_URL}/api/users/${userId}/ratings`, {
        credentials: 'include',
      })

      return { success: true, ratings: Array.isArray(response) ? response : [] }
    } catch (e: any) {
      console.error('Error fetching ratings:', e)
      
      let errorMessage = 'Failed to fetch ratings'
      
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
    submitRating,
    getUserRatings,
  }
}