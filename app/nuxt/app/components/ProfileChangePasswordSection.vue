<script setup lang="ts">
const toast = useToast();
const isRequesting = ref(false);

const handleChangePassword = async () => {
  if (isRequesting.value) return;

  isRequesting.value = true;

  try {
    const response = await useRequestChangePasswordCode();

    toast.add({
      title: response.messageTitle || 'Verification Code Sent!',
      description: response.message || 'Please check your email for the verification code.',
      color: 'success',
    });

    await new Promise((resolve) => setTimeout(resolve, 1000));
    navigateTo('/change-password-code');
  } catch (error: any) {
    let errorMessage = 'An unexpected error occurred.';
    
    if (error?.data?.error) {
      errorMessage = error.data.error;
    } else if (error?.message) {
      errorMessage = error.message;
    }

    // Check if it's a Google account error
    const isGoogleError = errorMessage.includes('Google');

    toast.add({
      title: isGoogleError ? 'Cannot Change Password' : 'Request Failed',
      description: errorMessage,
      color: 'error',
    });
  } finally {
    isRequesting.value = false;
  }
};
</script>

<template>
  <div class="mt-6">
    <button
      @click="handleChangePassword"
      :disabled="isRequesting"
      class="px-6 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {{ isRequesting ? 'Sending Code...' : 'Change Password' }}
    </button>
  </div>
</template>