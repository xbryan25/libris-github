<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuthStore';

const openLogoutConfirmationModal = ref(false);

const toast = useToast();
const auth = useAuthStore();

const userLogout = async () => {
  try {
    const { messageTitle, message } = await auth.logout();

    toast.add({
      title: messageTitle,
      description: message,
      color: 'success',
    });

    navigateTo('/login');
  } catch (error) {
    toast.add({
      title: 'Login failed.',
      description: error.data.error,
      color: 'error',
    });
  }
};
</script>

<template>
  <UButton class="cursor-pointer" @click="openLogoutConfirmationModal = true">Logout?</UButton>

  <UModal v-model:open="openLogoutConfirmationModal">
    <template #content>
      <div class="flex flex-col gap-1 items-center w-full h-40 p-5">
        <h2 class="text-3xl font-semibold">Logout Confirmation</h2>
        <h3 class="text-md font-semibold text-muted">Are you sure you want to log out?</h3>

        <div class="flex gap-2 w-full pt-5 justify-center">
          <UButton
            size="md"
            color="error"
            variant="solid"
            class="cursor-pointer"
            @click="openLogoutConfirmationModal = false"
            >Cancel</UButton
          >
          <UButton
            size="md"
            color="primary"
            variant="solid"
            type="submit"
            class="cursor-pointer"
            @click="async () => await userLogout()"
            >Confirm</UButton
          >
        </div>
      </div>
    </template>
  </UModal>
</template>
