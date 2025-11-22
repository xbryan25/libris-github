<script setup lang="ts">
import guest from '~/middleware/guest';
import { useAuthStore } from '~/stores/useAuthStore';

import { googleAuthCodeLogin } from 'vue3-google-login';

definePageMeta({
  layout: 'unauthenticated',
  middleware: guest,
});

const toast = useToast();
const auth = useAuthStore();
const isLoading = ref(false);

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
    const googlePopupResponse = await googleAuthCodeLogin(); // may trigger COOP warning

    const code = googlePopupResponse.code;

    const { messageTitle, message } = await useUserGoogleLogin(code);

    toast.add({
      title: messageTitle,
      description: message,
      color: 'success',
    });

    // send code to backend, etc.
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
  </div>
</template>
