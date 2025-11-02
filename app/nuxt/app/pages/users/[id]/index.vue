<script setup lang="ts">
import auth from '~/middleware/auth';
import { onMounted } from 'vue';
import { useProfile } from '~/composables/UseProfile';
import ProfileMainSection from '~/components/ProfileMainSection.vue';
import ProfileAdditionalInfo from '~/components/ProfileAdditionalInfo.vue';

const route = useRoute();
const userId = route.params.id as string;

const { profile, fetchProfile, loading, error, isUserNotFound } = useProfile(userId);

definePageMeta({
  middleware: auth,
});

onMounted(() => {
  fetchProfile();
});
</script>

<template>
  <div class="min-h-screen w-full py-10 px-4 md:px-8 lg:px-15">
    <div
      v-if="isUserNotFound"
      class="flex items-center justify-center h-screen"
    >
      <UCard class="bg-surface border-base max-w-md">
        <div class="text-center p-6">
          <UIcon
            name="i-heroicons-exclamation-triangle"
            class="w-16 h-16 text-yellow-500 mx-auto mb-4"
          />
          <h2 class="text-2xl font-bold text-base mb-2">
            User Not Found
          </h2>
          <p class="text-muted mb-4">
            The user you're trying to view does not exist or may have been removed.
          </p>
          <NuxtLink
            to="/users/me"
            class="px-6 py-2 bg-accent text-white rounded-lg hover:bg-accent/90 transition cursor-pointer"
          >
           <span> Go Back </span>
        </NuxtLink>
        </div>
      </UCard>
    </div>
    <div v-else class="mt-20 gap-10 flex flex-col justify-center items-center">
      <ProfileMainSection :profile="profile" :loading="loading" :error="error" :user-id="userId" />
      <ProfileAdditionalInfo :profile="profile" :loading="loading" :error="error" />
      <ProfileLibraryDetails
        :profile="profile"
        :loading="loading"
        :error="error"
        :user-id="userId"
      />
    </div>
  </div>
</template>
