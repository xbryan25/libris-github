<script setup lang="ts">
import { validateNewUsername } from '#imports';
import { useAuthStore } from '~/stores/useAuthStore';

const props = defineProps<{
  userId: string | null;
  isOpenAddUsernameModal: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:openAddUsernameModal', value: boolean): void;
  (e: 'addUsernameSuccess'): void;
}>();

const newUsername = ref('');
const isSubmittingNewUsername = ref(false);

const auth = useAuthStore();
const toast = useToast();

const isOpenAddUsernameModal = computed({
  get: () => props.isOpenAddUsernameModal,
  set: (val: boolean) => {
    emit('update:openAddUsernameModal', val);
  },
});

const submitNewUsername = async () => {
  try {
    isSubmittingNewUsername.value = true;

    const { messageTitle, message } = await useSubmitNewUsername(props.userId, newUsername.value);

    toast.add({
      title: messageTitle,
      description: message,
      color: 'success',
    });

    auth.username = newUsername.value;

    emit('addUsernameSuccess');
  } catch (error) {
    toast.add({
      title: 'Username update failed.',
      description: error.data.error,
      color: 'error',
    });

    isSubmittingNewUsername.value = false;
  }
};
</script>

<template>
  <UModal v-model:open="isOpenAddUsernameModal">
    <template #header>
      <h2 class="text-3xl font-semibold">Add Username</h2>
    </template>

    <template #body>
      <div class="flex flex-col gap-5">
        <div class="flex gap-1">
          <p class="text-sm">Note:</p>
          <p class="text-sm">
            Your account has been created, but you need to provide your username to continue.
          </p>
        </div>

        <UForm
          :validate="(newUsername) => validateNewUsername(newUsername, isOpenAddUsernameModal)"
          :state="newUsername"
          class="space-y-4"
          @submit="async () => await submitNewUsername()"
        >
          <UFormField label="Username" name="username">
            <UInput v-model="newUsername" class="w-full" :disabled="isSubmittingNewUsername" />
          </UFormField>

          <div class="flex justify-end gap-2 w-full">
            <UButton
              size="md"
              color="error"
              variant="solid"
              class="cursor-pointer"
              @click="isOpenAddUsernameModal = false"
              >Cancel</UButton
            >
            <UButton
              size="md"
              color="primary"
              variant="solid"
              class="cursor-pointer"
              type="submit"
              :disabled="isSubmittingNewUsername"
              :loading="isSubmittingNewUsername"
              >Add Username</UButton
            >
          </div>
        </UForm>
      </div>
    </template>
  </UModal>
</template>
