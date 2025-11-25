<script setup lang="ts">
import guest from '~/middleware/guest';
import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  layout: 'unauthenticated',
  middleware: guest,
});

const toast = useToast();
const auth = useAuthStore();

const isDisabled = ref(false);
const isLoading = ref(false);

const onSubmitSignup = async (username: string, emailAddress: string, password: string) => {
  if (isLoading.value) return;

  isDisabled.value = true;
  isLoading.value = true;

  try {
    const { messageTitle, message } = await auth.signup(username, emailAddress, password);
    toast.add({
      title: messageTitle,
      description: message,
      color: 'success',
    });
    navigateTo('/login');
  } catch (error: any) {
    let errorMessage = 'An unexpected error occurred.';

    if (error.data?.error) {
      errorMessage = error.data.error;
    } else if (error.message) {
      errorMessage = error.message;
    }

    toast.add({
      title: 'Signup failed.',
      description: errorMessage,
      color: 'error',
    });
  } finally {
    isDisabled.value = false;
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="h-screen w-full flex overflow-hidden bg-background text-base">
    <div class="flex-1 flex items-center justify-center">
      <AuthForm
        auth-type="signup"
        :is-loading="isLoading"
        @on-submit-signup="(username, email, password) => onSubmitSignup(username, email, password)"
      />
    </div>
    <div class="flex-1">
      <NuxtImg src="/images/authImage1.jpg" class="w-full h-full object-cover" alt="Auth image" />
    </div>
  </div>
</template>
