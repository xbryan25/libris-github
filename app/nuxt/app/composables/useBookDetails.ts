import { ref, computed } from 'vue'

type BookDetails = {
  book_id: string
  title: string
  author: string
  genres: string[]
  condition: string
  description: string
  availability: 'rent' | 'purchase' | 'both'
  daily_rent_price: number
  security_deposit: number
  purchase_price: number
  rental_duration: number
  owner_user_id: string
  owner_username: string
  owner_profile_picture: string
  owner_trust_score: number
  times_rented: number
  is_rented: boolean
  is_purchased: boolean
  images: string[]
}

type AvailabilityBadge = {
  label: string
  color: string
}

type TrustScoreBadge = {
  text: string
  color: string
}

const API_URL = import.meta.env.VITE_API_URL

export const useBookDetails = () => {
  const book = ref<BookDetails | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)

  const { $apiFetch } = useNuxtApp();

  const fetchBookDetails = async (bookId: string) => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<BookDetails>(`${API_URL}/api/books/${bookId}`, {
        credentials: 'include'
      })
      book.value = res
    } catch (e: any) {
      error.value = e?.message || 'Failed to fetch book details'
      throw e
    } finally {
      loading.value = false
    }
  }

  const availabilityBadges = computed<AvailabilityBadge[]>(() => {
    if (!book.value) return []
    
    const badges: AvailabilityBadge[] = []
    
    if (book.value.availability === 'rent' || book.value.availability === 'both') {
      badges.push({ label: 'For Rent', color: 'blue' })
    }
    
    if (book.value.availability === 'purchase' || book.value.availability === 'both') {
      badges.push({ label: 'For Sale', color: 'red' })
    }
    
    return badges
  })

  const ownerTrustBadge = computed<TrustScoreBadge>(() => {
    if (!book.value) return { text: 'Unknown', color: 'bg-zinc-500' }
    
    const score = book.value.owner_trust_score
    
    if (score >= 951) return { text: 'Perfect', color: 'bg-[#15803D]' }
    if (score >= 751) return { text: 'Exceptional', color: 'bg-[#22C55E]' }
    if (score >= 500) return { text: 'Good', color: 'bg-[#84CC16]' }
    if (score >= 251) return { text: 'Decent', color: 'bg-[#FACC15]' }
    if (score >= 51) return { text: 'Bad', color: 'bg-[#CA8A04]' }
    return { text: 'Poor', color: 'bg-[#000000]' }
  })

  return {
    book,
    loading,
    error,
    fetchBookDetails,
    availabilityBadges,
    ownerTrustBadge
  }
}