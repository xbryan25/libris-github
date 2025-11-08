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
</script>

<template>
  <div class="h-screen w-full flex overflow-hidden bg-background text-base">
    <div class="flex-1 flex items-center justify-center">
      <AuthForm
        auth-type="login"
        :is-loading="isLoading"
        @on-submit-login="(email, password) => onSubmitLogin(email, password)"
      />
    </div>

    <div class="flex-1">
      <NuxtImg src="/images/authImage1.jpg" class="w-full h-full object-cover" alt="Auth image" />
    </div>
  </div>
</template>
