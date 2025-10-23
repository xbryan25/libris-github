import { ref, reactive } from 'vue'
import type { Profile } from '~/composables/UseProfile'

const API_URL = import.meta.env.VITE_API_URL

export const useProfileEdit = () => {
    const isEditing = ref(false)
    const saving = ref(false)
    const error = ref<string | null>(null)
    const success = ref<string | null>(null)

    const editForm = reactive({
        first_name: '',
        middle_name: '',
        last_name: '',
        date_of_birth: '',
        phone_number: '',
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
        editForm.date_of_birth = new Date().toISOString().split('T')[0]
        editForm.phone_number = profile.phone_number || ''

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

            const response = await fetch(`${API_URL}/api/users/profile/me`, {
                method: 'PUT',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSave)
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.message || 'Failed to update profile')
            }

            const result = await response.json()
            success.value = result.message || 'Profile updated successfully'
            isEditing.value = false

            return editForm
        } catch (e: any) {
            error.value = e.message || 'Failed to update profile'
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
        saveProfile
    }
}
