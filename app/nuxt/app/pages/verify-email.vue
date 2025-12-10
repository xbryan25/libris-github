<script setup lang="ts">
import guest from '~/middleware/guest';
import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  layout: 'unauthenticated',
  middleware: guest,
});

const route = useRoute();
const router = useRouter();
const toast = useToast();
const auth = useAuthStore();

const isLoading = ref(false);
const isResending = ref(false);
const resendCooldown = ref(0);
const userId = ref((route.query.userId as string) || '');
const code = ref(['', '', '', '', '', '']);
const codeInputs = ref<HTMLInputElement[]>([]);
let cooldownInterval: NodeJS.Timeout | null = null;

if (!userId.value) {
  console.log('[VERIFY-EMAIL] No userId found, redirecting to signup');
  navigateTo('/signup');
}

console.log('[VERIFY-EMAIL] Page loaded with userId:', userId.value);

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
  console.log('[VERIFY-EMAIL] Starting cooldown for', seconds, 'seconds');
  resendCooldown.value = seconds;

  if (cooldownInterval) {
    clearInterval(cooldownInterval);
  }

  cooldownInterval = setInterval(() => {
    resendCooldown.value -= 1;

    if (resendCooldown.value <= 0) {
      console.log('[VERIFY-EMAIL] Cooldown completed');
      clearInterval(cooldownInterval!);
      cooldownInterval = null;
    }
  }, 1000);
};

const getResendButtonText = () => {
  if (isResending.value) {
    return 'Sending...';
  }
  if (resendCooldown.value > 0) {
    return `Wait ${resendCooldown.value}s`;
  }
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

  try {
    console.log(
      '[VERIFY-EMAIL] Calling useVerifyEmailCode with userId:',
      userId.value,
      'code:',
      fullCode,
    );
    const response = await useVerifyEmailCode(userId.value, fullCode);

    console.log('[VERIFY-EMAIL] Verify response:', response);

    toast.add({
      title: response?.messageTitle || 'Email Verified!',
      description: response?.message || 'Your email has been successfully verified.',
      color: 'success',
    });

    // await new Promise((resolve) => setTimeout(resolve, 1500));
    navigateTo('/dashboard');
  } catch (error: any) {
    console.error('[VERIFY-EMAIL] Verification error:', error);

    let errorMessage = 'An unexpected error occurred.';

    if (error?.data?.error) {
      errorMessage = error.data.error;
    } else if (error?.message) {
      errorMessage = error.message;
    } else if (error?.error) {
      errorMessage = error.error;
    }

    toast.add({
      title: 'Verification failed.',
      description: errorMessage,
      color: 'error',
    });

    code.value = ['', '', '', '', '', ''];
    focusInput(0);

    isLoading.value = false;
  }
};

const resendCode = async () => {
  console.log('[VERIFY-EMAIL] Resend button clicked');
  console.log('[VERIFY-EMAIL] isResending:', isResending.value);
  console.log('[VERIFY-EMAIL] resendCooldown:', resendCooldown.value);

  // Prevent multiple clicks during cooldown or loading
  if (isResending.value || resendCooldown.value > 0) {
    console.log('[VERIFY-EMAIL] Resend blocked - already in progress or on cooldown');
    if (resendCooldown.value > 0) {
      const minutes = Math.ceil(resendCooldown.value / 60);
      const message = `Please wait for ${minutes} minute${minutes > 1 ? 's' : ''} before resending the code again, thank you.`;
      console.log('[VERIFY-EMAIL] Showing cooldown message:', message);
      toast.add({
        title: 'Please wait',
        description: message,
        color: 'error',
      });
    }
    return;
  }

  isResending.value = true;
  console.log('[VERIFY-EMAIL] Starting resend process for userId:', userId.value);

  try {
    console.log('[VERIFY-EMAIL] Calling useResendVerificationCode...');

    const response = await useResendVerificationCode(userId.value);

    console.log('[VERIFY-EMAIL] Resend response:', response);

    toast.add({
      title: response?.messageTitle || 'Code Resent!',
      description: response?.message || 'A new verification code has been sent to your email.',
      color: 'success',
    });

    // Clear inputs after resend
    code.value = ['', '', '', '', '', ''];
    focusInput(0);

    // Start 60-second cooldown
    startCooldown(60);
  } catch (error: any) {
    let errorMessage = 'Failed to resend code.';

    if (error?.data?.error) {
      errorMessage = error.data.error;
    } else if (error?.message) {
      errorMessage = error.message;
    } else if (error?.error) {
      errorMessage = error.error;
    }

    toast.add({
      title: 'Resend failed.',
      description: errorMessage,
      color: 'error',
    });
  } finally {
    isResending.value = false;
    console.log('[VERIFY-EMAIL] Resend process completed');
  }
};

const goToLoginPage = async () => {
  await useUserLogout();

  auth.username = null;
  auth.userId = null;
  auth.isAuthenticated = false;
  auth.isEmailVerified = false;

  router.push('/login');
};

onMounted(() => {
  console.log('[VERIFY-EMAIL] Component mounted');
  focusInput(0);
});

onUnmounted(() => {
  console.log('[VERIFY-EMAIL] Component unmounted');
  if (cooldownInterval) {
    clearInterval(cooldownInterval);
  }
});
</script>

<template>
  <div class="w-full min-h-screen flex flex-col bg-background text-base">
    <!-- Header -->
    <header class="w-full p-6 flex justify-between items-center">
      <div class="flex gap-3 items-center">
        <Icon name="icons:logo" class="w-12 h-12" />
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white">Libris</h1>
        <!-- <h1 class="text-5xl font-extrabold">Libris</h1> -->
      </div>
      <ColorModeButton />
    </header>

    <!-- Back to login link -->
    <div class="w-full px-6 mb-4">
      <button
        class="text-sm font-semibold text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white flex items-center gap-2 transition-colors cursor-pointer"
        @click="goToLoginPage"
      >
        <Icon name="heroicons:arrow-left" class="w-5 h-5" />
        Back to login
      </button>
    </div>

    <!-- Main Content -->
    <main class="flex-grow flex items-center justify-center p-4">
      <div class="rounded-3xl p-10 w-full max-w-xl flex flex-col items-center text-center">
        <!-- Envelope Icon with Check -->
        <div class="relative mb-6 inline-block">
          <Icon name="heroicons:envelope" class="w-26 h-26 text-gray-900 dark:text-white" />
          <div
            class="absolute -top-2 -right-2 bg-white dark:bg-neutral-900 rounded-full border-4 border-white dark:border-neutral-900 flex items-center justify-center"
          >
            <Icon name="heroicons:check-circle-solid" class="w-10 h-10 text-green-500" />
          </div>
        </div>

        <!-- Heading -->
        <h2 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-4">Check your inbox</h2>
        <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
          We've sent a 6-digit code to your email.<br />
          Please enter it below to continue.
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
          class="w-full h-12 rounded-xl cursor-pointer justify-center text-lg font-bold bg-green-600 hover:bg-green-700 text-white"
          :disabled="isLoading"
          :loading="isLoading"
          @click="verifyCode"
        >
          {{ isLoading ? 'Verifying...' : 'Verify' }}
        </UButton>

        <!-- Resend Code Link -->
        <div class="flex gap-1 text-base mt-6">
          <p class="text-gray-600 dark:text-gray-400">Didn't Receive it?</p>
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
