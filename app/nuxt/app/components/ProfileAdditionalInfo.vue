<script setup lang="ts">
import { computed } from 'vue'
import type { Profile } from '~/composables/UseProfile'
import { useProfileEdit } from '~/composables/useProfileEdit'

interface Props {
  profile: Profile | null
  loading: boolean
  error: string | null
  isCurrentUser?: boolean // Whether this is the current user's profile
  isEditing?: boolean // Whether we're in edit mode
  editForm?: any // The edit form data
}

const props = defineProps<Props>()

const emit = defineEmits<{
  startEdit: []
  save: []
  cancel: []
}>()

const editForm = computed(() => props.editForm || {})
</script>

<template>
  <UCard v-if="loading" class="w-[1500px] h-[350px] bg-surface border-base flex items-stretch px-10">
    <div class="flex w-full items-start justify-between space-x-10">
      <div class="flex flex-col w-1/2 space-y-8">
        <USkeleton class="h-10 w-64" />
        <div class="grid grid-cols-3 gap-x-20 gap-y-8">
          <div class="flex flex-col space-y-2">
            <USkeleton class="h-8 w-24" />
            <USkeleton class="h-6 w-32" />
          </div>
          <div class="flex flex-col space-y-2">
            <USkeleton class="h-8 w-28" />
            <USkeleton class="h-6 w-28" />
          </div>
          <div class="flex flex-col space-y-2">
            <USkeleton class="h-8 w-20" />
            <USkeleton class="h-6 w-30" />
          </div>
          <div class="flex flex-col space-y-2">
            <USkeleton class="h-8 w-28" />
            <USkeleton class="h-6 w-24" />
          </div>
          <div class="flex flex-col space-y-2">
            <USkeleton class="h-8 w-32" />
            <USkeleton class="h-6 w-36" />
          </div>
        </div>
      </div>

      <USeparator orientation="vertical" class="h-[300px]" type="solid" />

      <div class="flex flex-col w-1/2 space-y-8">
        <USkeleton class="h-10 w-32" />
        <div class="grid grid-cols-3 gap-x-20 gap-y-8">
          <div class="flex flex-col space-y-2">
            <USkeleton class="h-8 w-20" />
            <USkeleton class="h-6 w-24" />
          </div>
          <div class="flex flex-col space-y-2">
            <USkeleton class="h-8 w-16" />
            <USkeleton class="h-6 w-20" />
          </div>
          <div class="flex flex-col space-y-2">
            <USkeleton class="h-8 w-24" />
            <USkeleton class="h-6 w-28" />
          </div>
          <div class="flex flex-col space-y-2">
            <USkeleton class="h-8 w-20" />
            <USkeleton class="h-6 w-32" />
          </div>
          <div class="flex flex-col space-y-2">
            <USkeleton class="h-8 w-28" />
            <USkeleton class="h-6 w-20" />
          </div>
        </div>
      </div>
    </div>
  </UCard>
  
  <div v-else-if="error" class="w-[1500px] h-[350px] bg-surface border-base flex items-center justify-center">
    <div class="text-lg text-red-500">Error: {{ error }}</div>
  </div>

  <UCard v-else class="w-[1500px] h-[350px] bg-surface border-base flex items-stretch px-10">
    <div class="flex w-full items-start justify-between space-x-10">

      <div class="flex flex-col w-1/2 space-y-8">
        <div class="text-[32px] font-bold text-base">Personal Information</div>
        <div class="grid grid-cols-3 gap-x-20 gap-y-8">
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">First Name</div>
            <div v-if="!isEditing" class="text-[20px] text-muted">{{profile?.first_name}}</div>
            <UInput v-else v-model="editForm.first_name" placeholder="First Name" />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Middle Name</div>
            <div v-if="!isEditing" class="text-[20px] text-muted">{{profile?.middle_name}}</div>
            <UInput v-else v-model="editForm.middle_name" placeholder="Middle Name" />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Last Name</div>
            <div v-if="!isEditing" class="text-[20px] text-muted">{{profile?.last_name}}</div>
            <UInput v-else v-model="editForm.last_name" placeholder="Last Name" />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Date of Birth</div>
            <div v-if="!isEditing" class="text-[20px] text-muted">{{profile?.date_of_birth}}</div>
            <UInput v-else v-model="editForm.date_of_birth" type="date" />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base whitespace-nowrap">Phone Number</div>
            <div v-if="!isEditing" class="text-[20px] text-muted">{{profile?.phone_number}}</div>
            <UInput v-else v-model="editForm.phone_number" placeholder="Phone Number" />
          </div>
        </div>
      </div>

      <USeparator orientation="vertical" class="h-[300px]" type="solid" />

      <div class="flex flex-col w-1/2 space-y-8">
        <div class="flex justify-between items-center">
          <div class="text-[32px] font-bold text-base">Address</div>
          <div class="flex items-center space-x-2">
            <UButton 
              v-if="isCurrentUser && !isEditing"
              @click="$emit('startEdit')"
              icon="i-heroicons-pencil"
              color="primary"
              variant="solid"
              size="sm"
            />
            <div v-if="isCurrentUser && isEditing" class="flex space-x-2">
              <UButton 
                @click="$emit('save', editForm)"
                color="primary"
                size="sm"
              >
                Save
              </UButton>
              <UButton 
                @click="$emit('cancel')"
                color="neutral"
                variant="outline"
                size="sm"
              >
                Cancel
              </UButton>
            </div>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-x-20 gap-y-8">
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Country</div>
            <div v-if="!isEditing" class="text-[20px] text-muted">{{profile?.address?.country}}</div>
            <UInput v-else v-model="editForm.address.country" placeholder="Country" />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">City</div>
            <div v-if="!isEditing" class="text-[20px] text-muted">{{profile?.address?.city}}</div>
            <UInput v-else v-model="editForm.address.city" placeholder="City" />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Barangay</div>
            <div v-if="!isEditing" class="text-[20px] text-muted">{{profile?.address?.barangay}}</div>
            <UInput v-else v-model="editForm.address.barangay" placeholder="Barangay" />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Street</div>
            <div v-if="!isEditing" class="text-[20px] text-muted">{{profile?.address?.street}}</div>
            <UInput v-else v-model="editForm.address.street" placeholder="Street" />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Postal Code</div>
            <div v-if="!isEditing" class="text-[20px] text-muted">{{profile?.address?.postal_code}}</div>
            <UInput v-else v-model="editForm.address.postal_code" placeholder="Postal Code" />
          </div>
        </div>
      </div>
    </div>
  </UCard>
</template>
