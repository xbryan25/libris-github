import { ref } from 'vue'

type Address = {
  street: string
  barangay: string
  city: string
  country: string
  postal_code: string
}

export type Profile = {
  username: string
  first_name: string
  middle_name: string
  last_name: string
  date_of_birth: string
  phone_number: string
  account_activated_at: string
  address?: Address
  trust_score: number
  profile_image_url?: string
}

const API_URL = import.meta.env.VITE_API_URL

export const useProfile = (userId?: string) => {
  const profile = ref<Profile | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchProfile = async () => {
    loading.value = true
    error.value = null
    try {
      const url = userId
        ? `${API_URL}/api/users/profile/${userId}`
        : `${API_URL}/api/users/profile/me`

      const options: any = {
        credentials: 'include'
      }

      const res = await $fetch<Profile>(url, options)
      res.account_activated_at = new Date(res.account_activated_at).toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      })
      res.date_of_birth = new Date(res.date_of_birth).toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      })
      profile.value = res
    } catch (e: any) {
      error.value = e?.message || 'Failed to fetch profile info'
    } finally {
      loading.value = false
    }
  }

  return { profile, loading, error, fetchProfile }
}
