import { ref, reactive } from 'vue'
import type { Profile } from '~/composables/UseProfile'

const API_URL = import.meta.env.VITE_API_URL

export const useProfileEdit = () => {
  // Separate edit states for personal info and address
  const isEditingPersonal = ref(false)
  const isEditingAddress = ref(false)

  // Separate loading states
  const savingPersonal = ref(false)
  const savingAddress = ref(false)

  // Separate error states
  const errorPersonal = ref<string | null>(null)
  const errorAddress = ref<string | null>(null)

  // Separate success states
  const successPersonal = ref<string | null>(null)
  const successAddress = ref<string | null>(null)

  // Legacy states for backward compatibility (if needed)
  const isEditing = ref(false)
  const saving = ref(false)
  const error = ref<string | null>(null)
  const success = ref<string | null>(null)

  const toast = useToast()

  const { $apiFetch } = useNuxtApp()

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
      postal_code: '',
      latitude: null as number | null,
      longitude: null as number | null
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
      editForm.address.latitude = profile.address.latitude || null
      editForm.address.longitude = profile.address.longitude || null
    }
  }

  const startEditingPersonal = (profile: Profile | null) => {
    initializeForm(profile)
    isEditingPersonal.value = true
    errorPersonal.value = null
    successPersonal.value = null
  }

  const startEditingAddress = (profile: Profile | null) => {
    initializeForm(profile)
    isEditingAddress.value = true
    errorAddress.value = null
    successAddress.value = null
  }

  const cancelEditingPersonal = () => {
    isEditingPersonal.value = false
    errorPersonal.value = null
    successPersonal.value = null
  }

  const cancelEditingAddress = () => {
    isEditingAddress.value = false
    errorAddress.value = null
    successAddress.value = null
  }

  const savePersonalInfo = async (formData?: any) => {
    savingPersonal.value = true
    errorPersonal.value = null
    successPersonal.value = null

    try {
      const dataToSave = formData || {
        first_name: editForm.first_name,
        middle_name: editForm.middle_name,
        last_name: editForm.last_name,
        date_of_birth: editForm.date_of_birth,
        phone_number: editForm.phone_number
      }

      const filteredData = JSON.parse(JSON.stringify(dataToSave, (key, value) => {
        if (typeof value === 'string') return value.trim()
        if (value === undefined || value === null) return undefined
        return value
      }))

      const response = await $apiFetch(`${API_URL}/api/users/profile/me/personal`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filteredData)
      }) as { message?: string }

      successPersonal.value = response.message || 'Personal information updated successfully'

      toast.add({
        title: 'Success',
        description: successPersonal.value ?? '',
        color: 'success',
      })

      isEditingPersonal.value = false

      return editForm
    } catch (e: any) {
      savingPersonal.value = false

      errorPersonal.value = e.message || 'Failed to update personal information'
      toast.add({
        title: 'Error',
        description: errorPersonal.value ?? 'Failed to update personal information',
        color: 'error',
      })
      throw e
    }
  }

  const saveAddress = async (formData?: any) => {
    savingAddress.value = true
    errorAddress.value = null
    successAddress.value = null

    try {
      const dataToSave = formData || editForm.address

      const filteredData = JSON.parse(JSON.stringify(dataToSave, (key, value) => {
        if (typeof value === 'string') return value.trim()
        if (value === undefined) return undefined;
        return value
      }))

      const response = await $apiFetch(`${API_URL}/api/users/profile/me/address`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filteredData)
      }) as { message?: string }

      successAddress.value = response.message || 'Address updated successfully'

      toast.add({
        title: 'Success',
        description: successAddress.value ?? '',
        color: 'success',
      })

      isEditingAddress.value = false

      return editForm
    } catch (e: any) {
      savingAddress.value = false

      errorAddress.value = e.message || 'Failed to update address'
      toast.add({
        title: 'Error',
        description: errorAddress.value ?? 'Failed to update address',
        color: 'error',
      })
      throw e
    }
  }

  // Legacy methods for backward compatibility
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

      const response = await $apiFetch(`${API_URL}/api/users/profile/me`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filteredData)
      }) as { message?: string }

      success.value = response.message || 'Profile updated successfully'

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
      await $apiFetch(`${API_URL}/api/users/profile/me`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile_image_url: imageUrl })
      })

      editForm.profile_image_url = imageUrl
      success.value = 'Profile picture updated successfully'
    } catch (e: any) {
      error.value = e.message || 'Failed to update profile picture'
    } finally {
      saving.value = false
    }
  }

  return {
    // Separate states
    isEditingPersonal,
    isEditingAddress,
    savingPersonal,
    savingAddress,
    errorPersonal,
    errorAddress,
    successPersonal,
    successAddress,
    // Separate methods
    startEditingPersonal,
    startEditingAddress,
    cancelEditingPersonal,
    cancelEditingAddress,
    savePersonalInfo,
    saveAddress,
    // Legacy states and methods (for backward compatibility)
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
