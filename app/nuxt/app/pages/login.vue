<script setup lang="ts">
import guest from '~/middleware/guest';
import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  layout: 'unauthenticated',
  middleware: guest,
});

const toast = useToast();
const auth = useAuthStore();
const isLoading = ref(false);

const isOpenAddUsernameModal = ref(false);

const onSubmitLogin = async (emailAddress: string, password: string) => {
  if (isLoading.value) return;

  isLoading.value = true;

  try {
    const { messageTitle, message } = await auth.login(emailAddress, password);

    toast.add({
      title: messageTitle,
      description: message,
      color: 'success',
    });

    navigateTo('/dashboard');
  } catch (error) {
    toast.add({
      title: 'Login failed.',
      description: error.data.error,
      color: 'error',
    });

    isLoading.value = false;
  }
};

const onSubmitGmailLogin = async () => {
  try {
    const { messageTitle, message } = await auth.googleLogin();

    if (auth.username === null) {
      isOpenAddUsernameModal.value = true;
    } else {
      toast.add({
        title: messageTitle,
        description: message,
        color: 'success',
      });

      navigateTo('/dashboard');
    }
  } catch (error) {
    toast.add({
      title: 'Login via Google failed.',
      description: error.data.error,
      color: 'error',
    });
  }
};

const onAddUsernameSuccess = async () => {
  try {
    navigateTo('/dashboard');
  } catch (error) {
    toast.add({
      title: 'Login via Google failed.',
      description: error.data.error,
      color: 'error',
    });
  }
};
</script>

<template>
  <div class="h-screen w-full flex overflow-hidden bg-background text-base">
    <div class="flex-1 flex items-center justify-center">
      <AuthForm
        auth-type="login"
        :is-loading="isLoading"
        @on-submit-login="(email, password) => onSubmitLogin(email, password)"
        @on-submit-gmail-login="async () => await onSubmitGmailLogin()"
      />
    </div>

    <div class="flex-1">
      <NuxtImg src="/images/authImage1.jpg" class="w-full h-full object-cover" alt="Auth image" />
    </div>

    <AddUsernameModal
      :user-id="auth.userId"
      :is-open-add-username-modal="isOpenAddUsernameModal"
      @update:open-add-username-modal="
        (newOpenAddUsernameModal) => (isOpenAddUsernameModal = newOpenAddUsernameModal)
      "
      @add-username-success="onAddUsernameSuccess"
    />
  </div>
</template>
