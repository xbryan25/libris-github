<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});

const route = useRoute();
const toast = useToast();
const isLoading = ref(false);
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

const code = ref((route.query.code as string) || '');
const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

const { validatePassword } = usePasswordValidation();

if (!code.value) {
  console.log('[CHANGE PASSWORD] No code found, redirecting');
  navigateTo('/users/me');
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
    currentPassword.value.length >= 8 &&
    passwordValidation.value.valid &&
    passwordsMatch.value &&
    !isLoading.value
  );
});

const onSubmitChangePassword = async () => {
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
    console.log('[CHANGE PASSWORD] Changing password');
    const response = await useChangePassword(code.value, currentPassword.value, newPassword.value);
    console.log('[CHANGE PASSWORD] Response:', response);

    toast.add({
      title: response.messageTitle || 'Password Changed!',
      description: response.message || 'Your password has been successfully changed.',
      color: 'success',
    });

    await new Promise((resolve) => setTimeout(resolve, 1500));
    navigateTo('/users/me');
  } catch (error: any) {
    console.error('[CHANGE PASSWORD] Error:', error);
    let errorMessage = 'An unexpected error occurred.';
    if (error.data?.error) {
      errorMessage = error.data.error;
    } else if (error.message) {
      errorMessage = error.message;
    }

    toast.add({
      title: 'Change Password Failed',
      description: errorMessage,
      color: 'error',
    });
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="flex-1 w-full flex flex-col bg-background">
    <!-- Main Content - Centered -->
    <main class="flex-grow flex items-center justify-center p-4">
      <div class="p-10 w-full max-w-xl">
        <!-- Heading -->
        <div class="mb-8 text-center">
          <h2 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-3">
            Change your password
          </h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">
            Enter your current password and choose a new strong password.
          </p>
        </div>

        <!-- Form -->
        <form class="space-y-5" @submit.prevent="onSubmitChangePassword">
          <!-- Current Password -->
          <div class="space-y-2">
            <label
              for="currentPassword"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Current Password
            </label>
            <UInput
              id="currentPassword"
              v-model="currentPassword"
              :type="showCurrentPassword ? 'text' : 'password'"
              placeholder="Enter current password"
              class="w-full"
              :disabled="isLoading"
              :ui="{ trailing: 'pe-1' }"
              required
            >
              <template #trailing>
                <UButton
                  color="neutral"
                  variant="link"
                  size="sm"
                  :icon="showCurrentPassword ? 'heroicons:eye-slash' : 'heroicons:eye'"
                  :disabled="isLoading"
                  @click="showCurrentPassword = !showCurrentPassword"
                />
              </template>
            </UInput>
          </div>

          <!-- New Password -->
          <div class="space-y-2">
            <label
              for="newPassword"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              New Password
            </label>
            <UInput
              id="newPassword"
              v-model="newPassword"
              :type="showNewPassword ? 'text' : 'password'"
              placeholder="Enter new password"
              class="w-full"
              :disabled="isLoading"
              :ui="{ trailing: 'pe-1' }"
              required
            >
              <template #trailing>
                <UButton
                  color="neutral"
                  variant="link"
                  size="sm"
                  :icon="showNewPassword ? 'heroicons:eye-slash' : 'heroicons:eye'"
                  :disabled="isLoading"
                  @click="showNewPassword = !showNewPassword"
                />
              </template>
            </UInput>
            <PasswordStrengthMeter :password="newPassword" :show-errors="false" />
            <div
              v-if="newPassword.length >= 8 && !passwordValidation.valid"
              class="mt-2 text-sm text-red-500 dark:text-red-400 flex items-start gap-1"
            >
              <Icon name="heroicons:exclamation-circle-solid" class="w-5 h-5 flex-shrink-0" />
              <span>One special character, number and uppercase letter needed</span>
            </div>
          </div>

          <!-- Confirm Password -->
          <div class="space-y-2">
            <label
              for="confirmPassword"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Confirm New Password
            </label>
            <UInput
              id="confirmPassword"
              v-model="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="Re-enter new password"
              class="w-full"
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
                  :disabled="isLoading"
                  @click="showConfirmPassword = !showConfirmPassword"
                />
              </template>
            </UInput>
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
            class="w-full h-12 rounded-xl cursor-pointer justify-center text-lg font-bold bg-green-600 hover:bg-green-700 text-white"
            :disabled="!canSubmit"
            :loading="isLoading"
          >
            {{ isLoading ? 'Changing Password...' : 'Change Password' }}
          </UButton>

          <!-- Cancel Link -->
          <div class="text-center mt-4">
            <NuxtLink
              to="/users/me"
              class="text-sm text-violet-700 dark:text-violet-400 hover:text-violet-800 dark:hover:text-violet-300 transition-colors"
            >
              Cancel and go back to profile
            </NuxtLink>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<style>
::-ms-reveal {
  display: none;
}
</style>
