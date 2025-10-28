import { ref, reactive } from 'vue'
import type { Profile } from '~/composables/UseProfile'

const API_URL = import.meta.env.VITE_API_URL

export const useProfileEdit = () => {
  const isEditing = ref(false)
  const saving = ref(false)
  const error = ref<string | null>(null)
  const success = ref<string | null>(null)
  const toast = useToast()

  const editForm = reactive({
    first_name: '',
    middle_name: '',
    last_name: '',
    date_of_birth: '',
    phone_number: '',
    profile_image_url: '',
    address: {
      country: '',
      city: '',
      barangay: '',
      street: '',
      postal_code: ''
    }
  })

  const initializeForm = (profile: Profile | null) => {
    if (!profile) return

    editForm.first_name = profile.first_name || ''
    editForm.middle_name = profile.middle_name || ''
    editForm.last_name = profile.last_name || ''
    editForm.date_of_birth = profile.date_of_birth || ''
    editForm.phone_number = profile.phone_number || ''
    editForm.profile_image_url = profile.profile_image_url || ''

    if (profile.address) {
      editForm.address.country = profile.address.country || ''
      editForm.address.city = profile.address.city || ''
      editForm.address.barangay = profile.address.barangay || ''
      editForm.address.street = profile.address.street || ''
      editForm.address.postal_code = profile.address.postal_code || ''
    }
  }

  const startEditing = (profile: Profile | null) => {
    initializeForm(profile)
    isEditing.value = true
    error.value = null
    success.value = null
  }

  const cancelEditing = () => {
    isEditing.value = false
    error.value = null
    success.value = null
  }

  const saveProfile = async (formData?: any) => {
    saving.value = true
    error.value = null
    success.value = null

    try {
      const dataToSave = formData || editForm

      const filteredData = JSON.parse(JSON.stringify(dataToSave, (key, value) => {
        if (typeof value === 'string') return value.trim() 
        if (value === undefined || value === null) return undefined
        return value
      }))

      const response = await fetch(`${API_URL}/api/users/profile/me`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filteredData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Failed to update profile')
      }

      const result = await response.json()
      success.value = result.message || 'Profile updated successfully'
      toast.add({
        title: 'Success',
        description: success.value ?? '',
        color: 'success',
      })
      isEditing.value = false

      return editForm
    } catch (e: any) {
      error.value = e.message || 'Failed to update profile'
      toast.add({
        title: 'Error',
        description: error.value ?? 'Failed to update profile',
        color: 'error',
      })
    } finally {
      saving.value = false
    }
  }

  const updateProfileImage = async (imageUrl: string) => {
    try {
      saving.value = true
      const response = await fetch(`${API_URL}/api/users/profile/me`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile_image_url: imageUrl })
      })

      if (!response.ok) throw new Error('Failed to update profile picture')

      editForm.profile_image_url = imageUrl
      success.value = 'Profile picture updated successfully'
    } catch (e: any) {
      error.value = e.message || 'Failed to update profile picture'
    } finally {
      saving.value = false
    }
  }

  return {
    isEditing,
    saving,
    error,
    success,
    editForm,
    startEditing,
    cancelEditing,
    saveProfile,
    updateProfileImage
  }
}
