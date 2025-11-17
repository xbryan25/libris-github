  <script setup lang="ts">
  import { computed, ref, watch, toRef } from 'vue';
  import type { Profile } from '~/composables/UseProfile';
  import { validatePersonalInfo, validateAddress } from '@/utils/validateProfileEdit';
  import { useAddressAutocomplete } from '~/composables/useAddressAutocomplete';

  const LOCATIONIQ_API_KEY = import.meta.env.LOCATIONIQ_API_KEY;

  const { addressQuery, suggestions, fetchSuggestions, selectSuggestion } = useAddressAutocomplete(LOCATIONIQ_API_KEY);

  function handleSelectSuggestion(item: any) {
    selectSuggestion(item, editForm.value.address);
  }


  const errorMapPersonal = ref<Record<string, string>>({});
  const errorMapAddress = ref<Record<string, string>>({});

  interface Props {
    profile: Profile | null;
    loading: boolean;
    error: string | null;
    isCurrentUser?: boolean; // Whether this is the current user's profile
    isEditingPersonal?: boolean; // Whether personal info is in edit mode
    isEditingAddress?: boolean; // Whether address is in edit mode
    editForm?: any; // The edit form data
    savingPersonal?: boolean; // Loading state for personal info save
    savingAddress?: boolean; // Loading state for address save
  }

  const props = defineProps<Props>();

  const emit = defineEmits<{
    startEditPersonal: [];
    startEditAddress: [];
    savePersonal: [];
    saveAddress: [];
    cancelPersonal: [];
    cancelAddress: [];
  }>();

  const editForm = computed(() => props.editForm || {});

  const isEditingPersonalRef = toRef(props, 'isEditingPersonal');
  const isEditingAddressRef = toRef(props, 'isEditingAddress');

  const hasClickedSavePersonal = ref(false);
  const hasClickedSaveAddress = ref(false);

  // Clear errors when editing is cancelled or when editing starts
  watch(isEditingPersonalRef, (isEditing) => {
    if (!isEditing) {
      errorMapPersonal.value = {};
    } else {
      hasClickedSavePersonal.value = false;
      errorMapPersonal.value = {};
    }
  });

  watch(isEditingAddressRef, (isEditing) => {
    if (!isEditing) {
      errorMapAddress.value = {};
    } else {
      hasClickedSaveAddress.value = false;
      errorMapAddress.value = {};
    }
  });

  // Real-time validation for personal info fields
  watch(
    () => editForm.value.first_name,
    () => {
      if (props.isEditingPersonal) {
        validatePersonalField('first_name');
      }
    },
  );

  watch(
    () => editForm.value.middle_name,
    () => {
      if (props.isEditingPersonal) {
        validatePersonalField('middle_name');
      }
    },
  );

  watch(
    () => editForm.value.last_name,
    () => {
      if (props.isEditingPersonal) {
        validatePersonalField('last_name');
      }
    },
  );

  watch(
    () => editForm.value.phone_number,
    () => {
      if (props.isEditingPersonal) {
        validatePersonalField('phone_number');
      }
    },
  );

  // Real-time validation for address fields
  watch(
    () => editForm.value.address?.country,
    () => {
      if (props.isEditingAddress) {
        validateAddressField('address.country');
      }
    },
  );
  watch(
    () => editForm.value.address?.street,
    (street) => {
      if (props.isEditingAddress) {
        addressQuery.value = street || '';
      }
    }
  );

  watch(addressQuery, (val) => {
    if (props.isEditingAddress && val) fetchSuggestions(val);
  });

  function validatePersonalField(field: string) {
    const tempState = {
      first_name: editForm.value.first_name,
      middle_name: editForm.value.middle_name,
      last_name: editForm.value.last_name,
      phone_number: editForm.value.phone_number,
    };
    const allErrors = validatePersonalInfo(tempState);
    const fieldError = allErrors.find((e) => e.name === field);
    if (fieldError) errorMapPersonal.value[field] = fieldError.message;
    else delete errorMapPersonal.value[field];
  }

  function validateAddressField(field: string) {
    const tempState = editForm.value.address || {};
    const allErrors = validateAddress(tempState);
    const fieldError = allErrors.find((e) => e.name === field);
    if (fieldError) errorMapAddress.value[field] = fieldError.message;
    else delete errorMapAddress.value[field];
  }

  function onSavePersonal() {
    hasClickedSavePersonal.value = true;

    const errors = validatePersonalInfo({
      first_name: editForm.value.first_name,
      middle_name: editForm.value.middle_name,
      last_name: editForm.value.last_name,
      phone_number: editForm.value.phone_number,
    });
    errorMapPersonal.value = Object.fromEntries(errors.map((e) => [e.name, e.message]));
    if (errors.length === 0) emit('savePersonal');
  }

  function onSaveAddress() {
    hasClickedSaveAddress.value = true;

    const errors = validateAddress(editForm.value.address || {});
    errorMapAddress.value = Object.fromEntries(errors.map((e) => [e.name, e.message]));
    if (errors.length === 0) emit('saveAddress');
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
        <div class="flex justify-between items-center">
          <div class="text-[32px] font-bold text-base">Personal Information</div>
          <div class="flex items-center space-x-2">
            <UButton
              v-if="isCurrentUser && !isEditingPersonal"
              icon="i-heroicons-pencil"
              color="primary"
              variant="solid"
              size="sm"
              @click="$emit('startEditPersonal')"
            />
            <div v-if="isCurrentUser && isEditingPersonal" class="flex space-x-2">
              <UButton
                color="primary"
                size="sm"
                :disabled="hasClickedSavePersonal"
                :loading="savingPersonal || hasClickedSavePersonal"
                @click="onSavePersonal"
              >
                Save
              </UButton>
              <UButton
                color="neutral"
                variant="outline"
                size="sm"
                :disabled="hasClickedSavePersonal"
                @click="$emit('cancelPersonal')"
              >
                Cancel
              </UButton>
            </div>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-10 gap-y-8 w-full">
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">First Name</div>
            <div
              v-if="!isEditingPersonal"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.first_name"
            >
              {{ profile?.first_name || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.first_name"
              @input="validatePersonalField('first_name')"
              placeholder="First Name"
              :color="errorMapPersonal.first_name ? 'error' : 'primary'"
              :disabled="hasClickedSavePersonal"
            />
            <span v-if="errorMapPersonal.first_name" class="text-red-500 text-sm">{{
              errorMapPersonal.first_name
            }}</span>
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Middle Name</div>
            <div
              v-if="!isEditingPersonal"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.middle_name"
            >
              {{ profile?.middle_name || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.middle_name"
              placeholder="Middle Name"
              :color="errorMapPersonal.middle_name ? 'error' : 'primary'"
              :disabled="hasClickedSavePersonal"
              @input="validatePersonalField('middle_name')"
            />
            <span v-if="errorMapPersonal.middle_name" class="text-red-500 text-sm">{{
              errorMapPersonal.middle_name
            }}</span>
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Last Name</div>
            <div
              v-if="!isEditingPersonal"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.last_name"
            >
              {{ profile?.last_name || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.last_name"
              placeholder="Last Name"
              :color="errorMapPersonal.last_name ? 'error' : 'primary'"
              :disabled="hasClickedSavePersonal"
              @input="validatePersonalField('last_name')"
            />
            <span v-if="errorMapPersonal.last_name" class="text-red-500 text-sm">{{
              errorMapPersonal.last_name
            }}</span>
          </div>
          <div class="flex flex-col min-w-0">
            <div class="text-[25px] font-semibold text-base">Date of Birth</div>
            <div
              v-if="!isEditingPersonal"
              class="text-[20px] text-muted overflow-hidden text-ellipsis whitespace-nowrap"
              :title="profile?.date_of_birth"
            >
              {{ profile?.date_of_birth || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.date_of_birth"
              type="date"
              :disabled="hasClickedSavePersonal"
            />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base whitespace-nowrap">Phone Number</div>
            <div
              v-if="!isEditingPersonal"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.phone_number"
            >
              {{ profile?.phone_number || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.phone_number"
              placeholder="Phone Number"
              :color="errorMapPersonal.phone_number ? 'error' : 'primary'"
              :disabled="hasClickedSavePersonal"
              @input="validatePersonalField('phone_number')"
            />
            <span v-if="errorMapPersonal.phone_number" class="text-red-500 text-sm">{{
              errorMapPersonal.phone_number
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
              v-if="isCurrentUser && !isEditingAddress"
              icon="i-heroicons-pencil"
              color="primary"
              variant="solid"
              size="sm"
              @click="$emit('startEditAddress')"
            />
            <div v-if="isCurrentUser && isEditingAddress" class="flex space-x-2">
              <UButton
                color="primary"
                size="sm"
                :disabled="hasClickedSaveAddress"
                :loading="savingAddress || hasClickedSaveAddress"
                @click="onSaveAddress"
              >
                Save
              </UButton>
              <UButton
                color="neutral"
                variant="outline"
                size="sm"
                :disabled="hasClickedSaveAddress"
                @click="$emit('cancelAddress')"
              >
                Cancel
              </UButton>
            </div>
          </div>
        </div>

        <!-- Autocomplete street input -->
        <div v-if="isEditingAddress" class="flex flex-col mb-2">
          <div class="text-[25px] font-semibold text-base">Search Address</div>
          <div class="relative">
            <UInput
              v-model="addressQuery"
              :disabled="hasClickedSaveAddress"
              placeholder="Search Address..."
            />
            <ul
              v-if="suggestions.length"
              class="absolute z-50 mt-1 bg-white dark:bg-zinc-800 border border-gray-300 dark:border-zinc-700 rounded w-full max-h-40 overflow-auto"
            >
              <li
                v-for="(item, i) in suggestions"
                :key="i"
                @click="handleSelectSuggestion(item)"
                class="p-2 cursor-pointer hover:bg-gray-200 dark:hover:bg-zinc-700"
              >
                {{ item.display_name }}
              </li>
            </ul>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-x-20 gap-y-8">
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Country</div>
            <div
              v-if="!isEditingAddress"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.address?.country"
            >
              {{ profile?.address?.country || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.address.country"
              placeholder="Country"
              :color="errorMapAddress['address.country'] ? 'error' : 'primary'"
              :disabled="hasClickedSaveAddress"
              @input="validateAddressField('address.country')"
            />
            <span v-if="errorMapAddress['address.country']" class="text-red-500 text-sm">{{
              errorMapAddress['address.country']
            }}</span>
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">City</div>
            <div
              v-if="!isEditingAddress"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.address?.city"
            >
              {{ profile?.address?.city || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.address.city"
              :disabled="hasClickedSaveAddress"
              placeholder="City"
            />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Barangay</div>
            <div
              v-if="!isEditingAddress"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.address?.barangay"
            >
              {{ profile?.address?.barangay || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.address.barangay"
              :disabled="hasClickedSaveAddress"
              placeholder="Barangay"
            />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Street</div>
            <div
              v-if="!isEditingAddress"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.address?.street"
            >
              {{ profile?.address?.street || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.address.street"
              :disabled="hasClickedSaveAddress"
              placeholder="Street"
            />
          </div>
          <div class="flex flex-col">
            <div class="text-[25px] font-semibold text-base">Postal Code</div>
            <div
              v-if="!isEditingAddress"
              class="text-[20px] text-muted truncate max-w-full"
              :title="profile?.address?.postal_code"
            >
              {{ profile?.address?.postal_code || '-' }}
            </div>
            <UInput
              v-else
              v-model="editForm.address.postal_code"
              :disabled="hasClickedSaveAddress"
              placeholder="Postal Code"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
