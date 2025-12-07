import { ref } from 'vue'

const API_URL = import.meta.env.VITE_API_URL

export const useCompletedRentalRating = () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const getCompletedRentalRatings = async (
    rentalId: string
  ): Promise<{ givenRating: number, givenComment: string, receivedRating: number, receivedComment: string } | null> => {
    loading.value = true
    error.value = null

    try {
      const response: 
      { given_rating: number, 
        given_comment: string, 
        received_rating: number, 
        received_comment: string } 

        = await $apiFetch(`${API_URL}/api/ratings/rental/${rentalId}`, {
        credentials: 'include',
      })

      return { givenRating: response.given_rating, 
              givenComment: response.given_comment, 
              receivedRating: response.received_rating, 
              receivedComment: response.received_comment }

    } catch (e: any) {
      console.error('Error fetching ratings:', e)

      return null
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    getCompletedRentalRatings
  }
}