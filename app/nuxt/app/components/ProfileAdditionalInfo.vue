<script setup lang="ts">
import { computed, ref, watch, toRef } from 'vue';
import type { Profile } from '~/composables/UseProfile';
import { useProfileEdit } from '~/composables/useProfileEdit';
import { validateProfileForm } from '@/utils/validateProfileEdit';

const errorMap = ref<Record<string, string>>({});

interface Props {
  profile: Profile | null;
  loading: boolean;
  error: string | null;
  isCurrentUser?: boolean; // Whether this is the current user's profile
  isEditing?: boolean; // Whether we're in edit mode
  editForm?: any; // The edit form data
}

const props = defineProps<Props>();

const emit = defineEmits<{
  startEdit: [];
  save: [];
  cancel: [];
}>();

const editForm = computed(() => props.editForm || {});

const isEditingRef = toRef(props, 'isEditing');

const hasClickedEditButton = ref(false);

// Clear errors when editing is cancelled or when editing starts
watch(isEditingRef, (isEditing) => {
  if (!isEditing) {
    errorMap.value = {};
  } else {
    hasClickedEditButton.value = false;

    errorMap.value = {};
  }
});

// Real-time validation for fields
watch(
  () => editForm.value.first_name,
  () => {
    validateField('first_name');
  },
);

watch(
  () => editForm.value.middle_name,
  () => {
    validateField('middle_name');
  },
);

watch(
  () => editForm.value.last_name,
  () => {
    validateField('last_name');
  },
);

watch(
  () => editForm.value.phone_number,
  () => {
    validateField('phone_number');
  },
);

watch(
  () => editForm.value.address?.country,
  () => {
    validateField('address.country');
  },
);

function validateField(field: string) {
  const tempState = { ...editForm.value };
  const allErrors = validateProfileForm(tempState);
  const fieldError = allErrors.find((e) => e.name === field);
  if (fieldError) errorMap.value[field] = fieldError.message;
  else delete errorMap.value[field];
}

function onSave() {
  hasClickedEditButton.value = true;

  const errors = validateProfileForm(editForm.value);
  errorMap.value = Object.fromEntries(errors.map((e) => [e.name, e.message]));
  if (errors.length === 0) emit('save');
}
</script>

<template>
  <UCard
    v-if="loading"
    class="w-full max-w-[1500px] h-[300px] bg-surface border-base flex flex-row items-stretch px-6 md:px-10"
  >
    <div class="flex-1 flex w-full items-start justify-between space-x-10">
      <div class="flex flex-col w-full md:w-1/2 space-y-8">
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

      <USeparator orientation="vertical" class="h-full w-5" type="solid" />

      <div class="flex-1 flex flex-col w-full md:w-1/2 space-y-8">
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

  <div
    v-else-if="error"
    class="w-[1500px] h-[350px] bg-surface border-base flex items-center justify-center"
  >
    <div class="text-lg text-red-500">Error: {{ error }}</div>
  </div>

  <div
    v-else
    class="w-full max-w-[1500px] h-auto bg-white dark:bg-zinc-950 border border-zinc-300 dark:border-zinc-800 border-radius rounded-lg flex flex-col md:flex-row items-stretch px-10 py-6"
  >
    <div class="flex flex-col md:flex-row w-full items-start justify-between gap-10">
      <div class="flex flex-col w-full md:w-1/2 space-y-8">
        <div class="text-[32px] font-bold text-base">Personal Information</div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-10 gap-y-8 w-full">
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">First Name</div>
            <div
              v-if="!isEditing"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.first_name"
            >
              {{ profile?.first_name || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.first_name"
              @input="validateField('first_name')"
              placeholder="First Name"
              :color="errorMap.first_name ? 'error' : 'primary'"
            />
            <span v-if="errorMap.first_name" class="text-red-500 text-sm">{{
              errorMap.first_name
            }}</span>
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Middle Name</div>
            <div
              v-if="!isEditing"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.middle_name"
            >
              {{ profile?.middle_name || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.middle_name"
              placeholder="Middle Name"
              :color="errorMap.middle_name ? 'error' : 'primary'"
              :disabled="hasClickedEditButton"
              @input="validateField('middle_name')"
            />
            <span v-if="errorMap.middle_name" class="text-red-500 text-sm">{{
              errorMap.middle_name
            }}</span>
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Last Name</div>
            <div
              v-if="!isEditing"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.last_name"
            >
              {{ profile?.last_name || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.last_name"
              placeholder="Last Name"
              :color="errorMap.last_name ? 'error' : 'primary'"
              :disabled="hasClickedEditButton"
              @input="validateField('last_name')"
            />
            <span v-if="errorMap.last_name" class="text-red-500 text-sm">{{
              errorMap.last_name
            }}</span>
          </div>
          <div class="flex flex-col min-w-0">
            <div class="text-[25px] font-semibold text-base">Date of Birth</div>
            <div
              v-if="!isEditing"
              class="text-[20px] text-muted overflow-hidden text-ellipsis whitespace-nowrap"
              :title="profile?.date_of_birth"
            >
              {{ profile?.date_of_birth || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.date_of_birth"
              type="date"
              :disabled="hasClickedEditButton"
            />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base whitespace-nowrap">Phone Number</div>
            <div
              v-if="!isEditing"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.phone_number"
            >
              {{ profile?.phone_number || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.phone_number"
              placeholder="Phone Number"
              :color="errorMap.phone_number ? 'error' : 'primary'"
              :disabled="hasClickedEditButton"
              @input="validateField('phone_number')"
            />
            <span v-if="errorMap.phone_number" class="text-red-500 text-sm">{{
              errorMap.phone_number
            }}</span>
          </div>
        </div>
      </div>

      <USeparator orientation="vertical" class="h-full" type="solid" />

      <div class="flex flex-col w-full md:w-1/2 space-y-8">
        <div class="flex justify-between items-center">
          <div class="text-[32px] font-bold text-base">Address</div>
          <div class="flex items-center space-x-2">
            <UButton
              v-if="isCurrentUser && !isEditing"
              icon="i-heroicons-pencil"
              color="primary"
              variant="solid"
              size="sm"
              @click="$emit('startEdit')"
            />
            <div v-if="isCurrentUser && isEditing" class="flex space-x-2">
              <UButton
                color="primary"
                size="sm"
                :disabled="hasClickedEditButton"
                :loading="hasClickedEditButton"
                @click="onSave"
              >
                Save
              </UButton>
              <UButton
                color="neutral"
                variant="outline"
                size="sm"
                :disabled="hasClickedEditButton"
                @click="$emit('cancel')"
              >
                Cancel
              </UButton>
            </div>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-x-20 gap-y-8">
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Country</div>
            <div
              v-if="!isEditing"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.address?.country"
            >
              {{ profile?.address?.country || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.address.country"
              placeholder="Country"
              :color="errorMap['address.country'] ? 'error' : 'primary'"
              :disabled="hasClickedEditButton"
              @input="validateField('address.country')"
            />
            <span v-if="errorMap['address.country']" class="text-red-500 text-sm">{{
              errorMap['address.country']
            }}</span>
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">City</div>
            <div
              v-if="!isEditing"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.address?.city"
            >
              {{ profile?.address?.city || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.address.city"
              :disabled="hasClickedEditButton"
              placeholder="City"
            />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Barangay</div>
            <div
              v-if="!isEditing"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.address?.barangay"
            >
              {{ profile?.address?.barangay || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.address.barangay"
              :disabled="hasClickedEditButton"
              placeholder="Barangay"
            />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Street</div>
            <div
              v-if="!isEditing"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.address?.street"
            >
              {{ profile?.address?.street || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.address.street"
              :disabled="hasClickedEditButton"
              placeholder="Street"
            />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Postal Code</div>
            <div
              v-if="!isEditing"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.address?.postal_code"
            >
              {{ profile?.address?.postal_code || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.address.postal_code"
              :disabled="hasClickedEditButton"
              placeholder="Postal Code"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
