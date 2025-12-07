<script setup lang="ts">
import guest from '~/middleware/guest';

definePageMeta({
  layout: 'unauthenticated',
  middleware: guest,
});

const toast = useToast();
const isLoading = ref(false);
const emailAddress = ref('');

const onSubmitForgotPassword = async () => {
  if (isLoading.value) return;

  if (!emailAddress.value) {
    toast.add({
      title: 'Email Required',
      description: 'Please enter your email address.',
      color: 'error',
    });
    return;
  }

  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(emailAddress.value)) {
    toast.add({
      title: 'Invalid Email',
      description: 'Please enter a valid email address.',
      color: 'error',
    });
    return;
  }

  isLoading.value = true;

  try {
    console.log('[FORGOT PASSWORD] Requesting password reset for:', emailAddress.value);
    const response = await useRequestPasswordReset(emailAddress.value);
    console.log('[FORGOT PASSWORD] Response:', response);

    toast.add({
      title: response.messageTitle || 'Reset Code Sent!',
      description: response.message || 'Please check your email for the reset code.',
      color: 'success',
    });

    const userId = response.userId;

    if (!userId) {
      console.warn('[FORGOT PASSWORD] No userId returned - email might not exist');
      // For security, we still show success message even if email doesn't exist
      await new Promise((resolve) => setTimeout(resolve, 1500));
      // Stay on same page or redirect to login
      return;
    }

    await new Promise((resolve) => setTimeout(resolve, 1500));
    navigateTo(`/reset-password-code?userId=${userId}`);
  } catch (error: any) {
    console.error('[FORGOT PASSWORD] Error:', error);
    let errorMessage = 'An unexpected error occurred.';
    let errorTitle = 'Request Failed';

    if (error.data?.error) {
      errorMessage = error.data.error;
      
      // Check if it's a Google account error
      if (errorMessage.includes('Google')) {
        errorTitle = 'Cannot Reset Password';
      }
    } else if (error.message) {
      errorMessage = error.message;
    }

    toast.add({
      title: errorTitle,
      description: errorMessage,
      color: 'error',
    });
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="max-h-screen w-full flex overflow-hidden bg-background text-base">
    <!-- Left Side - Form -->
    <div class="flex-1 flex items-center justify-center">
      <div class="flex flex-col gap-10 box-border px-[10%] pb-[10%] max-w-2xl w-full">
        <!-- Color Mode Button -->
        <div class="mr-auto"><ColorModeButton /></div>

        <!-- Logo -->
        <div class="flex gap-3">
          <Icon name="icons:logo" class="w-12 h-12" />
          <h1 class="text-5xl font-extrabold">Libris</h1>
        </div>

        <!-- Heading -->
        <div class="flex flex-col gap-1">
          <h2 class="text-3xl font-bold">Find your account</h2>
          <h3>Enter your email address to receive a password reset code.</h3>
        </div>

        <!-- Form -->
        <form @submit.prevent="onSubmitForgotPassword" class="w-100 flex flex-col gap-5">
          <!-- Email Input -->
          <div class="space-y-2">
            <label for="email" class="block text-sm font-medium">
              Email Address
            </label>
            <UInput
              id="email"
              v-model="emailAddress"
              type="email"
              placeholder="your.email@example.com"
              class="w-100"
              :disabled="isLoading"
              required
            />
          </div>

          <!-- Submit Button -->
          <UButton
            type="submit"
            class="w-100 h-9 cursor-pointer justify-center text-lg font-bold"
            :disabled="isLoading"
            :loading="isLoading"
          >
            {{ isLoading ? 'Sending...' : 'Send Reset Code' }}
          </UButton>

          <!-- Back to Login - ADDED THIS -->
          <div class="flex gap-1 justify-center">
            <p class="text-sm">Remember your password?</p>
            <NuxtLink
              to="/login"
              class="text-sm text-violet-700 dark:text-violet-500 cursor-pointer hover:text-violet-800 dark:hover:text-violet-400 transition-colors"
            >
              Back to Login
            </NuxtLink>
          </div>
        </form>
      </div>
    </div>

    <!-- Right Side Image -->
    <div class="flex-1">
      <NuxtImg src="/images/authImage1.jpg" class="w-full h-full object-cover" alt="Auth image" />
    </div>
  </div>
</template>