<script setup lang="ts">
import guest from '~/middleware/guest';
import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  middleware: guest,
});

const toast = useToast();
const auth = useAuthStore();

const onSubmitSignup = async (username: string, emailAddress: string, password: string) => {
  try {
    const { messageTitle, message } = await auth.signup(username, emailAddress, password);
    toast.add({
      title: messageTitle,
      description: message,
      color: 'success',
    });
    navigateTo('/login');
  } catch (error) {
    toast.add({
      title: 'Signup failed.',
      description: error.data.error,
      color: 'error',
    });
  }
};
</script>

<template>
  <div class="max-h-screen w-full flex overflow-hidden bg-background text-base">
    <div class="flex-1 flex items-center justify-center">
      <AuthForm
        auth-type="signup"
        @on-submit-signup="(username, email, password) => onSubmitSignup(username, email, password)"
      />
    </div>
    <div class="flex-1">
      <NuxtImg src="/images/authImage1.jpg" class="w-full h-full object-cover" alt="Auth image" />
    </div>
  </div>
</template>