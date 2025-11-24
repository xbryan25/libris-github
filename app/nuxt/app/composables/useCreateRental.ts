import { ref } from 'vue'

const API_URL = import.meta.env.VITE_API_URL

export const useCreateRental = () => {
  const rentalExists = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const toast = useToast()

  const { $apiFetch } = useNuxtApp()

  const checkRentalExists = async (bookId: string) => {
    try {
      const res = await $apiFetch<{ exists: boolean }>(
        `${API_URL}/api/rentals/check/${bookId}`,
        { method: 'GET', credentials: 'include' }
      )
      rentalExists.value = res.exists
    } catch (e: any) {
      console.error(e)
    }
  }

  const createRental = async (payload: {
    book_id: string
    total_rent_cost: number
    rental_duration_days: number
    meetup_time_window: string
    meetup_location: string
    meetup_date: string
  }) => {
    loading.value = true
    error.value = null

    try {
      await $apiFetch(`${API_URL}/api/wallets/update-reserved-amount`, {
        method: 'PATCH',
        body: { amount_to_reserve: payload.total_rent_cost },
        credentials: 'include'
      })

      const res = await $apiFetch(`${API_URL}/api/rentals/create`, {
        method: 'POST',
        body: payload,
        credentials: 'include'
      })

      toast.add({
        title: 'Success',
        description: 'Rental request sent successfully',
        color: 'success',
      })

      return res
    } catch (err: any) {
      error.value = err?.data?.message || err?.data?.error || err?.message || 'Failed to process rental'
      toast.add({
        title: 'Error',
        description: error.value ?? 'Failed to process rental',
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
    createRental,
    checkRentalExists,
    rentalExists
  }
}
