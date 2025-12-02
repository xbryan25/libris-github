import { ref, computed } from 'vue'

export type Rental = {
  rental_id: string
  rent_status: string
  book_id: string
  title: string
  author: string
  image: string
  from: string
  actual_deposit: number
  actual_rate: number
  all_fees_captured: boolean
  reserved_at: string
  reservation_expires_at: string
  rental_duration_days: number
  meetup_location: string
  meetup_time_window: string
  pickup_confirmation_started_at: string
  user_confirmed_pickup: boolean
  owner_confirmed_pickup: boolean
  return_confirmation_started_at: string
  user_confirmed_return: boolean
  owner_confirmed_return: boolean
  user_rated: boolean
  owner_rated: boolean
  cost: number
  meetup_date: string
  meetup_time: string
  rent_start_date: string
  rent_end_date: string
}

type RentalStatus = 
  | 'pending' 
  | 'approved' 
  | 'awaiting_pickup_confirmation' 
  | 'ongoing' 
  | 'awaiting_return_confirmation' 
  | 'completed'

type StatusBadge = {
  label: string
  color: string
  progress: number
}

type ProgressStep = {
  label: string
  status: RentalStatus
  completed: boolean
  active: boolean
}

const API_URL = import.meta.env.VITE_API_URL

export const useUserRentals = () => {
  const rentals = ref<Rental[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const fetchUserRentals = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<Rental[]>(`${API_URL}/api/rentals/my-rentals`, {
        credentials: 'include'
      })
      rentals.value = Array.isArray(res) ? res : []
    } catch (e: any) {
      rentals.value = []
      console.log('No rentals found or error fetching rentals:', e)
    } finally {
      loading.value = false
    }
  }

  const fetchUserCompletedRentals = async (sortBy: string, sortOrder: string, cardsPerPage: number, pageNumber: number) => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<Rental[]>(`${API_URL}/api/rentals/my-completed-rentals`, {
        credentials: 'include',
        query: {
          sortBy, sortOrder, cardsPerPage, pageNumber
        }
      })
      rentals.value = Array.isArray(res) ? res : []

      console.log(rentals.value)
    } catch (e: any) {
      rentals.value = []
      console.log('No rentals found or error fetching rentals:', e)
    } finally {
      loading.value = false
    }
  }

  const statusBadge = computed(() => (status: string): StatusBadge => {
    const statusConfig: Record<string, StatusBadge> = {
      pending: { label: 'Requested', color: 'bg-yellow-500', progress: 1 },
      approved: { label: 'Confirmed', color: 'bg-blue-500', progress: 2 },
      awaiting_pickup_confirmation: { label: 'Ready for Pickup', color: 'bg-orange-500', progress: 3 },
      ongoing: { label: 'Renting', color: 'bg-purple-500', progress: 4 },
      awaiting_return_confirmation: { label: 'Ready for Return', color: 'bg-indigo-500', progress: 5 },
      completed: { label: 'Completed', color: 'bg-green-500', progress: 6 }
    }
    
    return statusConfig[status] || { label: status, color: 'bg-gray-500', progress: 0 }
  })

  const progressSteps = computed(() => (rental: Rental): ProgressStep[] => {
    const currentProgress = statusBadge.value(rental.rent_status).progress
    
    const steps: { label: string; status: RentalStatus }[] = [
      { label: 'Requested', status: 'pending' },
      { label: 'Confirmed', status: 'approved' },
      { label: 'Pickup', status: 'awaiting_pickup_confirmation' },
      { label: 'Renting', status: 'ongoing' },
      { label: 'Return', status: 'awaiting_return_confirmation' },
      { label: 'Completed', status: 'completed' }
    ]
    
    return steps.map((step, index) => ({
      ...step,
      completed: index + 1 < currentProgress,
      active: index + 1 === currentProgress
    }))
  })

  const filteredRentals = computed(() => (statusFilter?: string) => {
    if (!statusFilter) return rentals.value
    return rentals.value.filter(rental => rental.rent_status === statusFilter)
  })

  const hasActiveRentals = computed(() => {
    return rentals.value.length > 0
  })

  return {
    rentals,
    loading,
    error,
    fetchUserRentals,
    fetchUserCompletedRentals,
    statusBadge,
    progressSteps,
    filteredRentals,
    hasActiveRentals
  }
}