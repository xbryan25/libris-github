<script setup lang="ts">
import auth from '~/middleware/auth';
import { onMounted } from 'vue'
import { useProfile } from '~/composables/UseProfile'
import { useProfileEdit } from '~/composables/useProfileEdit'
import ProfileMainSection from '~/components/ProfileMainSection.vue'
import ProfileAdditionalInfo from '~/components/ProfileAdditionalInfo.vue'

definePageMeta({
  middleware: auth,
});

const { profile, fetchProfile, loading, error } = useProfile()
const { isEditing, startEditing, saveProfile, cancelEditing, editForm } = useProfileEdit()

const handleStartEdit = () => {
  startEditing(profile.value)
}

const handleSave = async (formData: any) => {
  const updatedProfile = await saveProfile(formData)
  if (updatedProfile) {
    await fetchProfile()
  }
}

const handleCancel = () => {
  cancelEditing()
}

const handleProfileUpdate = async (updatedData: any) => {
  await fetchProfile()
}

const handleImageUpdate = async (imageUrl: string) => {
  await fetchProfile()
}

onMounted(() => {
  fetchProfile()
})
</script>

<template>
  <div class="min-h-screen w-full pt-4 px-4 md:px-8 lg:px-15">
    <div class="mt-20 gap-10 flex flex-col justify-center items-center">
      <ProfileMainSection 
        :profile="profile" 
        :loading="loading" 
        :error="error" 
        :is-current-user="true"
        :is-editing="isEditing"
        :edit-form="editForm"
        @profile-updated="handleProfileUpdate"
        @image-updated="handleImageUpdate"
      />
      <ProfileAdditionalInfo 
        :profile="profile" 
        :loading="loading" 
        :error="error" 
        :is-current-user="true"
        :is-editing="isEditing"
        :edit-form="editForm"
        @start-edit="handleStartEdit"
        @save="handleSave"
        @cancel="handleCancel"
      />
    </div>
  </div>
</template>
