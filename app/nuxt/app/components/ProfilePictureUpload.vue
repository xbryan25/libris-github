<script setup lang="ts">
import { ref, computed } from 'vue'
import { useProfilePictureUpload } from '~/composables/useProfilePictureUpload'

interface Props {
  currentImageUrl?: string
  userId: string
  onImageUpdate?: (newImageUrl: string) => void
}

const props = defineProps<Props>()
const emit = defineEmits<{
  imageUpdated: [imageUrl: string]
}>()

const { uploading, error, uploadProfilePicture, updateProfileImageUrl, deleteOldProfilePicture } = useProfilePictureUpload()

const fileInput = ref<HTMLInputElement>()
const previewUrl = ref<string | null>(null)

const currentImage = computed(() => previewUrl.value || props.currentImageUrl)

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (file) {
    // Create preview URL
    previewUrl.value = URL.createObjectURL(file)
  }
}

const handleUpload = async () => {
  const file = fileInput.value?.files?.[0]
  if (!file) return

  try {
    // Upload to Supabase
    const imageUrl = await uploadProfilePicture(file, props.userId)
    
    if (imageUrl) {
      // Update profile in database
      const success = await updateProfileImageUrl(imageUrl)
      
      if (success) {
        // Delete old image if it exists and is different
        if (props.currentImageUrl && props.currentImageUrl !== imageUrl) {
          await deleteOldProfilePicture(props.currentImageUrl)
        }
        
        // Clear preview and file input
        previewUrl.value = null
        if (fileInput.value) {
          fileInput.value.value = ''
        }
        
        // Emit success
        emit('imageUpdated', imageUrl)
        props.onImageUpdate?.(imageUrl)
      }
    }
  } catch (err) {
    console.error('Upload failed:', err)
  }
}

const handleCancel = () => {
  previewUrl.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const triggerFileSelect = () => {
  fileInput.value?.click()
}
</script>

<template>
  <div class="flex flex-col items-center space-y-4">
    <!-- Profile Image Display -->
    <div class="relative group">
      <div class="w-32 h-32 rounded-full overflow-hidden border-4 border-gray-200">
        <img 
          v-if="currentImage" 
          :src="currentImage" 
          :alt="`Profile picture`"
          class="w-full h-full object-cover"
        />
        <Icon v-else name="heroicons:user-circle" class="w-full h-full text-gray-400" />
      </div>
      
      <!-- Upload Button Overlay -->
      <button
        @click="triggerFileSelect"
        :disabled="uploading"
        class="absolute inset-0 bg-black bg-opacity-50 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center"
      >
        <Icon name="heroicons:camera" class="w-8 h-8" />
      </button>
    </div>

    <!-- File Input (Hidden) -->
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      @change="handleFileSelect"
      class="hidden"
    />

    <!-- Upload Controls -->
    <div v-if="previewUrl" class="flex space-x-2">
      <UButton
        @click="handleUpload"
        :loading="uploading"
        color="primary"
        size="sm"
      >
        {{ uploading ? 'Uploading...' : 'Upload' }}
      </UButton>
      <UButton
        @click="handleCancel"
        :disabled="uploading"
        color="gray"
        variant="outline"
        size="sm"
      >
        Cancel
      </UButton>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="text-red-500 text-sm text-center max-w-xs">
      {{ error }}
    </div>

    <!-- Upload Instructions -->
    <UTooltip text="Click the camera icon to upload a new profile picture. Supported: JPEG, PNG, WebP (max 5MB)">
      <UButton variant="ghost" size="sm" icon="i-heroicons-information-circle" />
    </UTooltip>
  </div>
</template>
