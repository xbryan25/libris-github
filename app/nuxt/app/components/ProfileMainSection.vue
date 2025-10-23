<script setup lang="ts">
import TrustScoreDetails from './TrustScoreDetails.vue'
import type { Profile } from '~/composables/UseProfile'

interface Props {
  profile: Profile | null
  loading: boolean
  error: string | null
}

defineProps<Props>()
</script>

<template>
  <UCard v-if="loading" class="w-[1500px] h-[250px] bg-surface border-base flex items-stretch px-10">
    <div class="flex items-center justify-start space-x-6 flex-grow">
      <USkeleton class="w-35 h-35 rounded-full" />
      
      <div class="flex flex-col justify-center space-y-3">
        <USkeleton class="h-12 w-64" />
        <USkeleton class="h-10 w-80" />
        <USkeleton class="h-8 w-48" />
      </div>

      <div class="flex items-center h-full">
        <USeparator orientation="vertical" class="h-[200px] border-base ml-130" type="solid" />
      </div>

      <div class="flex flex-col space-y-3">
        <div class="flex items-center space-x-2">
          <USkeleton class="h-10 w-32" />
          <USkeleton class="w-6 h-6 rounded-full" />
        </div>
        <div class="flex items-center space-x-3">
          <USkeleton class="h-12 w-20" />
          <USkeleton class="h-8 w-16 rounded-full" />
        </div>
        <USkeleton class="h-4 w-48" />
      </div>
    </div>
  </UCard>
  
  <div v-else-if="error" class="w-[1500px] h-[250px] bg-surface border-base flex items-center justify-center">
    <div class="text-lg text-red-500">Error: {{ error }}</div>
  </div>

  <UCard v-else class="w-[1500px] h-[250px] bg-surface border-base flex items-stretch px-10">
    <div class="flex items-center justify-start space-x-6 flex-grow">
      <Icon name="icons:exchange" class="w-35 h-35 rounded-full" />

      <div class="flex flex-col justify-center">
        <div class="text-[42px] font-bold text-base">{{profile?.username}}</div>
        <div class="text-[35px] font-bold text-base">{{profile?.first_name}} {{ profile?.middle_name?.charAt(0) }}. {{profile?.last_name}}</div>
        <div class="text-[25px] font-bold text-muted">Joined since {{profile?.account_activated_at}}</div>
      </div>

      <div class="flex items-center h-full">
        <USeparator orientation="vertical" class="h-[200px] border-base ml-130" type="solid" />
      </div>

      <div class="flex flex-col">
        <div class="flex items-center space-x-2">
          <div class="text-[38px] font-extrabold text-base">Trust Score</div>
          <TrustScoreDetails />
        </div>

        <div class="flex items-center space-x-3">
          <div class="text-[40px] font-semibold text-base">{{profile?.trust_score}}</div>
          <UBadge class="bg-[#FACC15] text-white text-center px-3 py-1" variant="solid">
            Decent
          </UBadge>
        </div>

        <div class="text-[15px] font-semibold text-muted">19% more than other people</div>
      </div>
    </div>
  </UCard>
</template>
