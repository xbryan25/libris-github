<script setup lang="ts">
import auth from '~/middleware/auth';
import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  middleware: auth,
});

const toast = useToast();
const authStore = useAuthStore();

const isLoading = ref(false);
const isResending = ref(false);
const resendCooldown = ref(0);
const code = ref(['', '', '', '', '', '']);
const codeInputs = ref<HTMLInputElement[]>([]);

let cooldownInterval: NodeJS.Timeout | null = null;

const focusInput = (index: number) => {
  if (codeInputs.value[index]) {
    codeInputs.value[index].focus();
  }
};

const handleInput = (index: number, event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = target.value;

  if (value.length > 1) {
    code.value[index] = value.slice(0, 1);
    target.value = code.value[index];
  } else {
    code.value[index] = value;
  }

  if (value && index < 5) {
    focusInput(index + 1);
  }
};

const handleKeyDown = (index: number, event: KeyboardEvent) => {
  if (event.key === 'Backspace' && !code.value[index] && index > 0) {
    focusInput(index - 1);
  }
};

const handlePaste = (event: ClipboardEvent) => {
  event.preventDefault();
  const pastedData = event.clipboardData?.getData('text') || '';
  const digits = pastedData.replace(/\D/g, '').slice(0, 6).split('');

  digits.forEach((digit, index) => {
    if (index < 6) {
      code.value[index] = digit;
    }
  });

  focusInput(Math.min(digits.length, 5));
};

const startCooldown = (seconds: number = 60) => {
  resendCooldown.value = seconds;
  if (cooldownInterval) {
    clearInterval(cooldownInterval);
  }

  cooldownInterval = setInterval(() => {
    resendCooldown.value -= 1;
    if (resendCooldown.value <= 0) {
      clearInterval(cooldownInterval!);
      cooldownInterval = null;
    }
  }, 1000);
};

const getResendButtonText = () => {
  if (isResending.value) return 'Sending...';
  if (resendCooldown.value > 0) return `Wait ${resendCooldown.value}s`;
  return 'Resend Code';
};

const verifyCode = async () => {
  if (isLoading.value) return;

  const fullCode = code.value.join('');
  if (fullCode.length !== 6) {
    toast.add({
      title: 'Invalid Code',
      description: 'Please enter all 6 digits.',
      color: 'error',
    });
    return;
  }

  isLoading.value = true;
  isResending.value = true;

  try {
    const response = await useVerifyChangePasswordCode(fullCode);

    toast.add({
      title: response?.messageTitle || 'Code Verified!',
      description: response?.message || 'You can now change your password.',
      color: 'success',
    });

    await new Promise((resolve) => setTimeout(resolve, 1000));

    authStore.allowedChangePassword = true;

    navigateTo(`/change-password-new?code=${fullCode}`);
  } catch (error: any) {
    let errorMessage = 'An unexpected error occurred.';

    if (error?.data?.error) {
      errorMessage = error.data.error;
    } else if (error?.message) {
      errorMessage = error.message;
    } else if (error?.error) {
      errorMessage = error.error;
    }

    toast.add({
      title: 'Verification Failed',
      description: errorMessage,
      color: 'error',
    });

    code.value = ['', '', '', '', '', ''];
    focusInput(0);

    isLoading.value = false;
    isResending.value = false;
  }
};

const resendCode = async () => {
  if (isResending.value || resendCooldown.value > 0) {
    if (resendCooldown.value > 0) {
      toast.add({
        title: 'Please wait',
        description: `Please wait ${Math.ceil(resendCooldown.value / 60)} minute(s) before resending.`,
        color: 'error',
      });
    }
    return;
  }

  isLoading.value = true;
  isResending.value = true;

  try {
    const response = await useResendChangePasswordCode();

    toast.add({
      title: response?.messageTitle || 'Code Resent!',
      description: response?.message || 'A new code has been sent to your email.',
      color: 'success',
    });

    code.value = ['', '', '', '', '', ''];
    focusInput(0);
    startCooldown(60);
  } catch (error: any) {
    let errorMessage = 'Failed to resend code.';
    if (error?.data?.error) {
      errorMessage = error.data.error;
    }

    toast.add({
      title: 'Resend Failed',
      description: errorMessage,
      color: 'error',
    });

    isLoading.value = false;
    isResending.value = false;
  }
};

onMounted(() => {
  focusInput(0);
});

onUnmounted(() => {
  if (cooldownInterval) {
    clearInterval(cooldownInterval);
  }
});
</script>

<template>
  <div class="flex-1 w-full h-full flex flex-col bg-background">
    <!-- Main Content - Centered -->
    <main class="flex-grow flex items-center justify-center p-4">
      <div class="rounded-3xl p-10 w-full max-w-xl flex flex-col items-center text-center">
        <!-- Shield Icon -->
        <div class="relative mb-6 inline-block">
          <Icon name="heroicons:shield-check" class="w-26 h-26 text-green-500" />
        </div>

        <!-- Heading -->
        <h2 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-4">
          Enter security code
        </h2>
        <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
          Please check your email for a message with your code.<br />
          Your code is 6 digits long.
        </p>

        <!-- Code Input Fields -->
        <div class="flex gap-3 mb-8">
          <input
            v-for="(digit, index) in code"
            :key="index"
            :ref="
              (el) => {
                if (el) codeInputs[index] = el as HTMLInputElement;
              }
            "
            v-model="code[index]"
            type="text"
            inputmode="numeric"
            maxlength="1"
            class="w-14 h-14 text-center text-2xl font-bold bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-xl border-none outline-none focus:ring-2 focus:ring-green-500 transition"
            :disabled="isLoading"
            @input="handleInput(index, $event)"
            @keydown="handleKeyDown(index, $event)"
            @paste="index === 0 ? handlePaste($event) : null"
          />
        </div>

        <!-- Verify Button -->
        <UButton
          @click="verifyCode"
          class="w-full h-12 rounded-xl cursor-pointer justify-center text-lg font-bold bg-green-600 hover:bg-green-700 text-white"
          :disabled="isLoading"
          :loading="isLoading"
        >
          {{ isLoading ? 'Verifying...' : 'Continue' }}
        </UButton>

        <!-- Resend Code Link -->
        <div class="flex gap-1 text-base mt-6">
          <p class="text-gray-600 dark:text-gray-400">Didn't receive the code?</p>
          <button
            class="text-gray-900 dark:text-white font-bold underline hover:text-green-600 dark:hover:text-green-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="isResending || resendCooldown > 0"
            @click="resendCode"
          >
            {{ getResendButtonText() }}
          </button>
        </div>
      </div>
    </main>
  </div>
</template>
