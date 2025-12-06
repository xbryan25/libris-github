import { ref, computed } from 'vue'

export type Sale = {
  purchase_id: string
  purchase_status: string
  original_owner_id: string
  user_id: string
  book_id: string
  title: string
  author: string
  image: string
  to: string
  all_fees_captured: boolean
  reserved_at: string
  reservation_expires_at: string
  meetup_location: string
  meetup_time_window: string
  meetup_time: string
  meetup_date: string
  pickup_confirmation_started_at: string
  user_confirmed_pickup: boolean
  owner_confirmed_pickup: boolean
  user_rated: boolean
  owner_rated: boolean
  cost: number
  transfer_decision_pending: boolean  
  ownership_transferred: boolean | null  
}

type PurchaseStatus = 
  | 'pending' 
  | 'approved' 
  | 'awaiting_pickup_confirmation' 
  | 'completed'

type StatusBadge = {
  label: string
  color: string
  progress: number
}

type ProgressStep = {
  label: string
  status: PurchaseStatus
  completed: boolean
  active: boolean
}

const API_URL = import.meta.env.VITE_API_URL

export const useUserSales = () => {
  const sales = ref<Sale[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const fetchUserSales = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<Sale[]>(`${API_URL}/api/purchases/my-sales`, {
        credentials: 'include'
      })
      sales.value = Array.isArray(res) ? res : []
    } catch (e: any) {
      sales.value = []
      console.log('No sales found or error fetching sales:', e)
    } finally {
      loading.value = false
    }
  }

  const fetchUserCompletedSales = async (sortOrder: string, cardsPerPage: number, pageNumber: number) => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<Sale[]>(`${API_URL}/api/purchases/my-completed-sales`, {
        credentials: 'include',
        query: {
          sortOrder, cardsPerPage, pageNumber
        }
      })
      sales.value = Array.isArray(res) ? res : []

      console.log(sales.value)
    } catch (e: any) {
      sales.value = []
      console.log('No sales found or error fetching sales:', e)
    } finally {
      loading.value = false
    }
  }

  const statusBadge = computed(() => (status: string): StatusBadge => {
    const statusConfig: Record<string, StatusBadge> = {
      pending: { label: 'Requested', color: 'bg-yellow-500', progress: 1 },
      approved: { label: 'Confirmed', color: 'bg-blue-500', progress: 2 },
      awaiting_pickup_confirmation: { label: 'Ready for Pickup', color: 'bg-orange-500', progress: 3 },
      completed: { label: 'Completed', color: 'bg-green-500', progress: 4 }
    }
    
    return statusConfig[status] || { label: status, color: 'bg-gray-500', progress: 0 }
  })

  const progressSteps = computed(() => (sale: Sale): ProgressStep[] => {
    const currentProgress = statusBadge.value(sale.purchase_status).progress
    
    const steps: { label: string; status: PurchaseStatus }[] = [
      { label: 'Pending', status: 'pending' },
      { label: 'Confirmed', status: 'approved' },
      { label: 'Delivered', status: 'awaiting_pickup_confirmation' },
      { label: 'Completed', status: 'completed' }
    ]
    
    return steps.map((step, index) => ({
      ...step,
      completed: index + 1 < currentProgress,
      active: index + 1 === currentProgress
    }))
  })

  const filteredSales = computed(() => (statusFilter?: string) => {
    if (!statusFilter) return sales.value
    return sales.value.filter(sale => sale.purchase_status === statusFilter)
  })

  const hasActiveSales = computed(() => {
    return sales.value.length > 0
  })

  return {
    sales,
    loading,
    error,
    fetchUserSales,
    fetchUserCompletedSales,
    statusBadge,
    progressSteps,
    filteredSales,
    hasActiveSales
  }
}