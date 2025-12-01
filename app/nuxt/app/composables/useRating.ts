import { ref } from 'vue'

const API_URL = import.meta.env.VITE_API_URL

/**
 * Composable for handling user ratings
 * 
 * Simple rating system that:
 * - Posts rating to user_ratings table
 * - Updates user_rated or owner_rated flag in rented_books
 */

export const useRating = () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const submitRating = async (
    rentalId: string,
    rating: number,
    review: string,
    from: 'rental' | 'lending'
  ): Promise<{ success: boolean; error?: string }> => {
    loading.value = true
    error.value = null

    try {
      await $apiFetch(`${API_URL}/api/ratings/${rentalId}/rate`, {
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