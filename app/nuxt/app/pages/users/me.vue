<script setup lang="ts">
import auth from '~/middleware/auth';
import { onMounted } from 'vue';
import { useProfile } from '~/composables/UseProfile';
import { useProfileEdit } from '~/composables/useProfileEdit';
import ProfileMainSection from '~/components/ProfileMainSection.vue';
import ProfileAdditionalInfo from '~/components/ProfileAdditionalInfo.vue';
import ProfileChangePasswordSection from '~/components/ProfileChangePasswordSection.vue';
import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  middleware: auth,
});

const { profile, fetchProfile, loading, error } = useProfile();

const authStore = useAuthStore();

const {
  isEditingPersonal,
  isEditingAddress,
  savingPersonal,
  savingAddress,
  startEditingPersonal,
  startEditingAddress,
  savePersonalInfo,
  saveAddress,
  cancelEditingPersonal,
  cancelEditingAddress,
  editForm,
  isEditing, // Legacy prop for ProfileMainSection
} = useProfileEdit();

const handleStartEditPersonal = () => {
  startEditingPersonal(profile.value);
};

const handleStartEditAddress = () => {
  startEditingAddress(profile.value);
};

const handleSavePersonal = async () => {
  try {
    await savePersonalInfo();
    await fetchProfile();
  } catch (e) {
    // Error is already handled in the composable
  }
};

const handleSaveAddress = async () => {
  try {
    await saveAddress();
    await fetchProfile();
  } catch (e) {
    // Error is already handled in the composable
  }
};

const handleCancelPersonal = () => {
  cancelEditingPersonal();
};

const handleCancelAddress = () => {
  cancelEditingAddress();
};

const handleProfileUpdate = async (updatedData: any) => {
  await fetchProfile();
};

const handleImageUpdate = async (imageUrl: string) => {
  await fetchProfile();
};

onMounted(() => {
  fetchProfile();
});
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
        :is-editing-personal="isEditingPersonal"
        :is-editing-address="isEditingAddress"
        :edit-form="editForm"
        :saving-personal="savingPersonal"
        :saving-address="savingAddress"
        @start-edit-personal="handleStartEditPersonal"
        @start-edit-address="handleStartEditAddress"
        @save-personal="handleSavePersonal"
        @save-address="handleSaveAddress"
        @cancel-personal="handleCancelPersonal"
        @cancel-address="handleCancelAddress"
      />

      <div class="flex gap-2">
        <LogoutButton />
        <ProfileChangePasswordSection v-if="authStore.isGoogleLogin == false" />
      </div>
    </div>
  </div>
</template>
