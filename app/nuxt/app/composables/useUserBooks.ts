import { ref } from 'vue'

type Book = {
  id: number
  title: string
  author: string
  image: string
  from?: string
  by?: string
  returnDate?: string
  cost: string
}

type BooksData = {
  renting: Book[]
  bought: Book[]
  'rented-by-others': Book[]
  'bought-by-others': Book[]
}

export const useBooks = () => {
  const { $apiFetch } = useNuxtApp();   

  const booksData = ref<BooksData>({
    renting: [],
    bought: [],
    'rented-by-others': [],
    'bought-by-others': []
  })
  
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchBooksData = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<BooksData>(`/api/books/my-books`, {
        credentials: 'include'
      })
      booksData.value = res
    } catch (e: any) {
      error.value = e?.message || 'Failed to fetch books data'
    } finally {
      loading.value = false
    }
  }

  const fetchRentingBooks = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<{ renting: Book[] }>(`/api/books/my-books/renting`, {
        credentials: 'include'
      })
      booksData.value.renting = res.renting
    } catch (e: any) {
      error.value = e?.message || 'Failed to fetch renting books'
    } finally {
      loading.value = false
    }
  }

  const fetchBoughtBooks = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<{ bought: Book[] }>(`/api/books/my-books/bought`, {
        credentials: 'include'
      })
      booksData.value.bought = res.bought
    } catch (e: any) {
      error.value = e?.message || 'Failed to fetch bought books'
    } finally {
      loading.value = false
    }
  }

  const fetchRentedByOthers = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<{ 'rented-by-others': Book[] }>(`/api/books/my-books/lent`, {
        credentials: 'include'
      })
      booksData.value['rented-by-others'] = res['rented-by-others']
    } catch (e: any) {
      error.value = e?.message || 'Failed to fetch rented by others books'
    } finally {
      loading.value = false
    }
  }

  const fetchBoughtByOthers = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $apiFetch<{ 'bought-by-others': Book[] }>(`/api/books/my-books/sold`, {
        credentials: 'include'
      })
      booksData.value['bought-by-others'] = res['bought-by-others']
    } catch (e: any) {
      error.value = e?.message || 'Failed to fetch bought by others books'
    } finally {
      loading.value = false
    }
  }

  return { 
    booksData, 
    loading, 
    error, 
    fetchBooksData,
    fetchRentingBooks,
    fetchBoughtBooks,
    fetchRentedByOthers,
    fetchBoughtByOthers
  }
}