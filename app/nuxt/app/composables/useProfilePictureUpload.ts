import { ref } from 'vue'

export const useProfilePictureUpload = (editForm: any) => {
    const uploading = ref(false)
    const error = ref<string | null>(null)
    const success = ref<string | null>(null)
    const progress = ref(0)
    const toast = useToast()

    const { $apiFetch } = useNuxtApp();

    const uploadProfilePicture = async (file: File, userId: string): Promise<string | null> => {
        uploading.value = true
        error.value = null
        progress.value = 0

        try {
            const { $supabase } = useNuxtApp()

            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
            if (!allowedTypes.includes(file.type)) throw new Error('Please upload a valid image file (JPEG, PNG, or WebP)')

            const maxSize = 5 * 1024 * 1024
            if (file.size > maxSize) throw new Error('File size must be less than 5MB')

            const fileExt = file.name.split('.').pop()
            const fileName = `profile-${userId}-${Date.now()}.${fileExt}`
            const filePath = `profile-pictures/${fileName}`

            const { error: uploadError } = await $supabase.storage
                .from('profile_images')
                .upload(filePath, file, {
                    cacheControl: '3600',
                    upsert: false,
                    contentType: file.type
                })

            if (uploadError) throw new Error(`Upload failed: ${uploadError.message}`)

            const { data: urlData } = $supabase.storage
                .from('profile_images')
                .getPublicUrl(filePath)

            if (!urlData?.publicUrl) throw new Error('Failed to get image URL')

            progress.value = 100
            return urlData.publicUrl

        } catch (err: any) {
            error.value = err.message || 'Upload failed'
            return null
        } finally {
            uploading.value = false
        }
    }

    const updateProfileImageUrl = async (imageUrl: string): Promise<boolean> => {
        try {
            const API_URL = import.meta.env.VITE_API_URL

            await $apiFetch(`${API_URL}/api/users/profile/me`, {
                method: 'PATCH',
                credentials: 'include',
                body: {
                    profile_image_url: imageUrl
                }

            })
            toast.add({
                title: 'Success',
                description: 'Profile picture updated successfully!',
                color: 'success',
            })
            

            return true
        } catch (err: any) {
            error.value = err.message || 'Failed to update profile'

            toast.add({
                title: 'Error',
                description: err.message || 'Failed to update profile',
                color: 'error',
            })

            return false
        }
    }

    const deleteOldProfilePicture = async (oldImageUrl: string): Promise<void> => {
        if (!oldImageUrl) return
        try {
            const { $supabase } = useNuxtApp()
            const fileName = oldImageUrl.split('/').pop()
            const filePath = `profile-pictures/${fileName}`
            await $supabase.storage.from('profile_images').remove([filePath])
        } catch (err) {
            console.warn('Failed to delete old profile picture:', err)
        }
    }

    return {
        uploading,
        error,
        success,
        progress,
        uploadProfilePicture,
        updateProfileImageUrl,
        deleteOldProfilePicture,
    }
}
