import { ref, computed } from 'vue'

export type Purchase = {
  purchase_id: string
  purchase_status: string
  original_owner_id: string
  user_id: string
  book_id: string
  title: string
  author: string
  image: string
  from: string
  all_fees_captured: boolean
  reserved_at: string
  reservation_expires_at: string
  meetup_location: string
  latitude: number
  longitude: number
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

export const useUserPurchases = () => {
  const purchases = ref<Purchase[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp()

  const fetchUserPurchases = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<Purchase[]>(`${API_URL}/api/purchases/my-purchases`, {
        credentials: 'include'
      })
      purchases.value = Array.isArray(res) ? res : []
    } catch (e: any) {
      purchases.value = []
      console.log('No purchases found or error fetching purchases:', e)
    } finally {
      loading.value = false
    }
  }

  const fetchUserCompletedPurchase = async (purchaseId: string) => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<Purchase>(`${API_URL}/api/purchases/completed-purchase/${purchaseId}`, {
        credentials: 'include',
      })
      purchases.value = [res]
    } catch (e: any) {
      purchases.value = []
      console.log('Completed purchase not found or error fetching completed purchase:', e)
    } finally {
      loading.value = false
    }
  }

  const fetchUserCompletedPurchases = async (sortOrder: string, cardsPerPage: number, pageNumber: number) => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<Purchase[]>(`${API_URL}/api/purchases/my-completed-purchases`, {
        credentials: 'include',
        query: {
          sortOrder, cardsPerPage, pageNumber
        }
      })
      purchases.value = Array.isArray(res) ? res : []

      console.log(purchases.value)
    } catch (e: any) {
      purchases.value = []
      console.log('No purchases found or error fetching purchases:', e)
    } finally {
      loading.value = false
    }
  }

  const statusBadge = computed(() => (status: string): StatusBadge => {
    const statusConfig: Record<string, StatusBadge> = {
      pending: { label: 'Pending Approval', color: 'bg-yellow-500', progress: 1 },
      approved: { label: 'Confirmed', color: 'bg-blue-500', progress: 2 },
      awaiting_pickup_confirmation: { label: 'Ready for Pickup', color: 'bg-orange-500', progress: 3 },
      completed: { label: 'Completed', color: 'bg-green-500', progress: 4 }
    }

    return statusConfig[status] || { label: status, color: 'bg-gray-500', progress: 0 }
  })

  const progressSteps = computed(() => (purchase: Purchase): ProgressStep[] => {
    const currentProgress = statusBadge.value(purchase.purchase_status).progress

    const steps: { label: string; status: PurchaseStatus }[] = [
      { label: 'Requested', status: 'pending' },
      { label: 'Confirmed', status: 'approved' },
      { label: 'Pickup', status: 'awaiting_pickup_confirmation' },
      { label: 'Completed', status: 'completed' }
    ]

    return steps.map((step, index) => ({
      ...step,
      completed: index + 1 < currentProgress,
      active: index + 1 === currentProgress
    }))
  })

  const filteredPurchases = computed(() => (statusFilter?: string) => {
    if (!statusFilter) return purchases.value
    return purchases.value.filter(purchase => purchase.purchase_status === statusFilter)
  })

  const hasActivePurchases = computed(() => {
    return purchases.value.length > 0
  })

  return {
    purchases,
    loading,
    error,
    fetchUserPurchases,
    fetchUserCompletedPurchase,
    fetchUserCompletedPurchases,
    statusBadge,
    progressSteps,
    filteredPurchases,
    hasActivePurchases
  }
}