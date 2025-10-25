<script setup lang="ts">
import { onMounted } from 'vue'
import { useProfile } from '~/composables/UseProfile'
import ProfileMainSection from '~/components/ProfileMainSection.vue'
import ProfileAdditionalInfo from '~/components/ProfileAdditionalInfo.vue'

const route = useRoute()
const userId = route.params.id as string

const { profile, fetchProfile, loading, error } = useProfile(userId)

onMounted(() => {
  fetchProfile()
})
</script>

<template>
  <div class="min-h-screen w-full pt-4 px-4 md:px-8 lg:px-15">
    <div class="mt-20 gap-10 flex flex-col justify-center items-center">
      <ProfileMainSection :profile="profile" :loading="loading" :error="error" :user-id="userId" />
      <ProfileAdditionalInfo :profile="profile" :loading="loading" :error="error" />
    </div>
  </div>
</template>