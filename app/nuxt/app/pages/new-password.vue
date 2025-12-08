<script setup lang="ts">
import guest from '~/middleware/guest';

definePageMeta({
  layout: 'unauthenticated',
  middleware: guest,
});

const route = useRoute();
const toast = useToast();
const isLoading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const userId = ref(route.query.userId as string || '');
const code = ref(route.query.code as string || '');
const newPassword = ref('');
const confirmPassword = ref('');

const { validatePassword } = usePasswordValidation();

if (!userId.value || !code.value) {
  console.log('[NEW PASSWORD] Missing userId or code, redirecting');
  navigateTo('/forgot-password');
}

const passwordValidation = computed(() => {
  if (!newPassword.value) {
    return { valid: false, errors: [], strength: 'weak' as const, percentage: 0 };
  }
  return validatePassword(newPassword.value);
});

const passwordsMatch = computed(() => {
  return newPassword.value === confirmPassword.value && confirmPassword.value.length > 0;
});

const canSubmit = computed(() => {
  return (
    passwordValidation.value.valid &&
    passwordsMatch.value &&
    !isLoading.value
  );
});

const onSubmitNewPassword = async () => {
  if (isLoading.value || !canSubmit.value) return;

  if (!passwordValidation.value.valid) {
    toast.add({
      title: 'Invalid Password',
      description: passwordValidation.value.errors[0] || 'Password does not meet requirements.',
      color: 'error',
    });
    return;
  }

  if (!passwordsMatch.value) {
    toast.add({
      title: 'Passwords Do Not Match',
      description: 'Please make sure both passwords are the same.',
      color: 'error',
    });
    return;
  }

  isLoading.value = true;

  try {
    console.log('[NEW PASSWORD] Resetting password for userId:', userId.value);
    const response = await useResetPassword(userId.value, code.value, newPassword.value);
    console.log('[NEW PASSWORD] Response:', response);

    toast.add({
      title: response.messageTitle || 'Password Reset!',
      description: response.message || 'Your password has been successfully reset.',
      color: 'success',
    });

    await new Promise((resolve) => setTimeout(resolve, 1500));
    navigateTo('/login');
  } catch (error: any) {
    console.error('[NEW PASSWORD] Error:', error);
    let errorMessage = 'An unexpected error occurred.';
    if (error.data?.error) {
      errorMessage = error.data.error;
    } else if (error.message) {
      errorMessage = error.message;
    }

    toast.add({
      title: 'Reset Failed',
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
          <h2 class="text-3xl font-bold">Choose a new password</h2>
          <h3>Create a strong password with at least 8 characters.</h3>
        </div>

        <!-- Form -->
        <form @submit.prevent="onSubmitNewPassword" class="w-100 flex flex-col gap-5">
          <!-- New Password Input -->
          <div class="space-y-2">
            <label for="newPassword" class="block text-sm font-medium">
              New Password
            </label>
            <UInput
              id="newPassword"
              v-model="newPassword"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Enter new password"
              class="w-100"
              :disabled="isLoading"
              :ui="{ trailing: 'pe-1' }"
              required
            >
              <template #trailing>
                <UButton
                  color="neutral"
                  variant="link"
                  size="sm"
                  :icon="showPassword ? 'heroicons:eye-slash' : 'heroicons:eye'"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                  :aria-pressed="showPassword"
                  :disabled="isLoading"
                  @click="showPassword = !showPassword"
                />
              </template>
            </UInput>

            <!-- Password Strength Meter -->
            <PasswordStrengthMeter :password="newPassword" :show-errors="false" />

            <!-- Error Message when password is 8+ chars but invalid -->
            <div
              v-if="newPassword.length >= 8 && !passwordValidation.valid"
              class="mt-2 text-sm text-red-500 dark:text-red-400 flex items-start gap-1"
            >
              <Icon name="heroicons:exclamation-circle-solid" class="w-5 h-5 flex-shrink-0" />
              <span>One special character, number and uppercase letter needed</span>
            </div>
          </div>

          <!-- Confirm Password Input -->
          <div class="space-y-2">
            <label for="confirmPassword" class="block text-sm font-medium">
              Confirm Password
            </label>
            <UInput
              id="confirmPassword"
              v-model="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="Re-enter new password"
              class="w-100"
              :disabled="isLoading"
              :ui="{ trailing: 'pe-1' }"
              required
            >
              <template #trailing>
                <UButton
                  color="neutral"
                  variant="link"
                  size="sm"
                  :icon="showConfirmPassword ? 'heroicons:eye-slash' : 'heroicons:eye'"
                  :aria-label="showConfirmPassword ? 'Hide password' : 'Show password'"
                  :aria-pressed="showConfirmPassword"
                  :disabled="isLoading"
                  @click="showConfirmPassword = !showConfirmPassword"
                />
              </template>
            </UInput>

            <!-- Passwords Match Indicator -->
            <div v-if="confirmPassword" class="mt-2 text-sm">
              <div v-if="passwordsMatch" class="flex items-center gap-2 text-green-500">
                <Icon name="heroicons:check-circle-solid" class="w-4 h-4" />
                <span>Passwords match</span>
              </div>
              <div v-else class="flex items-center gap-2 text-red-500">
                <Icon name="heroicons:x-circle-solid" class="w-4 h-4" />
                <span>Passwords do not match</span>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <UButton
            type="submit"
            class="w-100 h-9 cursor-pointer justify-center text-lg font-bold"
            :disabled="!canSubmit"
            :loading="isLoading"
          >
            {{ isLoading ? 'Resetting...' : 'Reset Password' }}
          </UButton>

          <!-- Back to Login Link -->
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