<script setup lang="ts">
import { onMounted } from 'vue'
import { useProfile } from '~/composables/useProfile'

const { profile, fetchProfile, loading, error } = useProfile()

onMounted(() => {
  fetchProfile()
})

</script>
<template>
    <UCard class="w-[1500px] h-[350px] bg-surface border-base flex items-stretch px-10">
      <div class="flex w-full items-start justify-between space-x-10">

        <div class="flex flex-col w-1/2 space-y-8">
          <div class="text-[32px] font-bold text-base">Personal Information</div>
          <div class="grid grid-cols-3 gap-x-20 gap-y-8">
            <div class="flex flex-col">
              <div class="text-[25px] font-semibold text-base">First Name</div>
              <div class="text-[20px] text-muted">{{profile?.first_name}}</div>
            </div>
            <div class="flex flex-col">
              <div class="text-[25px] font-semibold text-base">Middle Name</div>
              <div class="text-[20px] text-muted">{{profile?.middle_name}}</div>
            </div>
            <div class="flex flex-col">
              <div class="text-[25px] font-semibold text-base">Last Name</div>
              <div class="text-[20px] text-muted">{{profile?.last_name}}</div>
            </div>
            <div class="flex flex-col">
              <div class="text-[25px] font-semibold text-base">Date of Birth</div>
              <div class="text-[20px] text-muted">{{profile?.date_of_birth}}</div>
            </div>
            <div class="flex flex-col">
              <div class="text-[25px] font-semibold text-base whitespace-nowrap">Phone Number</div>
              <div class="text-[20px] text-muted">{{profile?.phone_number}}</div>
            </div>
          </div>
        </div>
  
        <USeparator orientation="vertical" class="h-[300px]" type="solid" />
  
        <div class="flex flex-col w-1/2 space-y-8">
          <div class="text-[32px] font-bold text-base">Address</div>
          <div class="grid grid-cols-3 gap-x-20 gap-y-8">
            <div class="flex flex-col">
              <div class="text-[25px] font-semibold text-base">Country</div>
              <div class="text-[20px] text-muted">{{profile?.address?.country}}</div>
            </div>
            <div class="flex flex-col">
              <div class="text-[25px] font-semibold text-base">City</div>
              <div class="text-[20px] text-muted">{{profile?.address?.city}}</div>
            </div>
            <div class="flex flex-col">
              <div class="text-[25px] font-semibold text-base">Barangay</div>
              <div class="text-[20px] text-muted">{{profile?.address?.barangay}}</div>
            </div>
            <div class="flex flex-col">
              <div class="text-[25px] font-semibold text-base">Street</div>
              <div class="text-[20px] text-muted">{{profile?.address?.street}}</div>
            </div>
            <div class="flex flex-col">
              <div class="text-[25px] font-semibold text-base">Postal Code</div>
              <div class="text-[20px] text-muted">{{profile?.address?.postal_code}}</div>
            </div>
          </div>
        </div>
      </div>
    </UCard>
  </template>
  