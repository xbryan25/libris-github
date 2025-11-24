import { ref, computed } from 'vue'

export type Lending = {
  rental_id: string
  rent_status: string
  book_id: string
  title: string
  author: string
  image: string
  to: string
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

export const useUserLendings = () => {
  const lendings = ref<Lending[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const fetchUserLendings = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<Lending[]>(`${API_URL}/api/rentals/my-lendings`, {
        credentials: 'include'
      })
      lendings.value = Array.isArray(res) ? res : []
    } catch (e: any) {
      lendings.value = []
      console.log('No lendings found or error fetching lendings:', e)
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

  const progressSteps = computed(() => (lending: Lending): ProgressStep[] => {
    const currentProgress = statusBadge.value(lending.rent_status).progress
    
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

  const filteredLendings = computed(() => (statusFilter?: string) => {
    if (!statusFilter) return lendings.value
    return lendings.value.filter(lending => lending.rent_status === statusFilter)
  })

  const hasActiveLendings = computed(() => {
    return lendings.value.length > 0
  })

  return {
    lendings,
    loading,
    error,
    fetchUserLendings,
    statusBadge,
    progressSteps,
    filteredLendings,
    hasActiveLendings
  }
}