<script setup lang="ts">
import type { FormSubmitEvent } from '@nuxt/ui';

const props = defineProps<{
  authType: string;
  isDisabled: boolean;
  isLoading: boolean;
  isLoadingGoogle?: boolean;
}>();

const emit = defineEmits<{
  (e: 'onSubmitLogin', email: string, password: string): void;
  (e: 'onSubmitSignup', username: string, email: string, password: string): void;
  (e: 'onSubmitGoogleLogin'): void;
}>();

const state = reactive({
  emailAddress: '',
  password: '',
  username: '',
  confirmPassword: '',
});

const showPassword = ref(false);
const showConfirmPassword = ref(false);

// Password validation for signup
const { validatePassword } = usePasswordValidation();

const passwordValidation = computed(() => {
  if (props.authType !== 'signup' || !state.password) {
    return { valid: false, errors: [], strength: 'weak' as const, percentage: 0 };
  }
  return validatePassword(state.password, state.username, state.emailAddress);
});

// Check if form can be submitted
const canSubmitSignup = computed(() => {
  if (props.authType !== 'signup') return true;

  return (
    state.username.length >= 3 &&
    state.emailAddress.length > 0 &&
    state.password.length >= 8 &&
    passwordValidation.value.valid &&
    state.confirmPassword === state.password
  );
});

const onSubmit = async (event: FormSubmitEvent<typeof state>) => {
  // For signup, check password validation before submitting
  if (props.authType === 'signup' && !passwordValidation.value.valid) {
    // Don't submit if password is invalid
    console.log('[AUTH FORM] Signup blocked - password validation failed');
    return;
  }

  if (props.authType === 'login') {
    emit('onSubmitLogin', event.data.emailAddress, event.data.password);
  } else if (props.authType === 'signup') {
    emit('onSubmitSignup', event.data.username, event.data.emailAddress, event.data.password);
  }
};
</script>

<template>
  <div class="flex flex-col gap-10 box-border px-[10%] pb-[10%] max-w-2xl w-full">
    <div class="mr-auto"><ColorModeButton /></div>
    <div class="flex gap-3">
      <Icon name="icons:logo" class="w-12 h-12" />
      <h1 class="text-5xl font-extrabold">Libris</h1>
    </div>
    <div class="flex flex-col gap-1">
      <h2 class="text-3xl font-bold">{{ authType === 'login' ? 'Login' : 'Sign Up' }}</h2>
      <h3>
        {{
          authType === 'login'
            ? 'Open the door to endless reading --- your next book awaits.'
            : 'Create your account and start your reading journey today.'
        }}
      </h3>
    </div>

    <div class="w-100 flex flex-col gap-5">
      <div v-if="authType === 'login'" class="flex flex-col gap-5">
        <UButton
          icon="logos:google-icon"
          label="Login with Google"
          class="justify-center bg-default border border-accented text-default cursor-pointer h-9 text-md font-bold hover:bg-muted active:bg-muted disabled:bg-elevated gap-3"
          :disabled="props.isDisabled"
          :loading="props.isLoadingGoogle"
          @click="emit('onSubmitGoogleLogin')"
        />
        <USeparator color="primary" size="sm" label="or" />
      </div>

      <UForm
        :validate="(state) => validateAuthForm(state, props.authType)"
        :state="state"
        class="space-y-4"
        @submit="(event) => onSubmit(event)"
      >
        <UFormField v-if="authType === 'signup'" label="Username" name="username">
          <UInput v-model="state.username" class="w-100" :disabled="props.isLoading" />
        </UFormField>

        <UFormField label="Email Address" name="emailAddress">
          <UInput
            v-model="state.emailAddress"
            class="w-100"
            :disabled="props.isLoading"
          />
        </UFormField>

        <UFormField label="Password" name="password">
          <UInput
            v-model="state.password"
            :type="showPassword ? 'text' : 'password'"
            class="w-100"
            :disabled="props.isLoading"
            :ui="{ trailing: 'pe-1' }"
          >
            <template #trailing>
              <UButton
                color="neutral"
                variant="link"
                size="sm"
                :icon="showPassword ? 'heroicons:eye-slash' : 'heroicons:eye'"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
                :aria-pressed="showPassword"
                :disabled="props.isLoading"
                @click="showPassword = !showPassword"
              />
            </template>
          </UInput>

          <!-- Password Strength Meter for Signup -->
          <template v-if="authType === 'signup'">
            <PasswordStrengthMeter :password="state.password" :show-errors="false" />

            <!-- Error Message when password is 8+ chars but invalid -->
            <div
              v-if="state.password.length >= 8 && !passwordValidation.valid"
              class="mt-2 text-sm text-red-500 dark:text-red-400 flex items-start gap-1"
            >
              <Icon name="heroicons:exclamation-circle-solid" class="w-5 h-5 flex-shrink-0" />
              <span>One special character, number and uppercase letter needed</span>
            </div>
          </template>
        </UFormField>

        <UFormField v-if="authType === 'signup'" label="Confirm Password" name="confirmPassword">
          <UInput
            v-model="state.confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            class="w-100"
            :disabled="props.isLoading"
            :ui="{ trailing: 'pe-1' }"
          >
            <template #trailing>
              <UButton
                color="neutral"
                variant="link"
                size="sm"
                :icon="showConfirmPassword ? 'heroicons:eye-slash' : 'heroicons:eye'"
                :aria-label="showConfirmPassword ? 'Hide password' : 'Show password'"
                :aria-pressed="showConfirmPassword"
                :disabled="props.isLoading"
                @click="showConfirmPassword = !showConfirmPassword"
              />
            </template>
          </UInput>
        </UFormField>

        <!-- Forgot Password Link for Login -->
        <div v-if="authType === 'login'" class="w-full">
          <NuxtLink
            to="/forgot-password"
            class="text-sm inline-block text-violet-700 dark:text-violet-500 hover:text-violet-800 dark:hover:text-violet-400 cursor-pointer transition-colors"
          >
            Forgot your password?
          </NuxtLink>
        </div>

        <UButton
          type="submit"
          class="w-100 h-9 cursor-pointer justify-center text-lg font-bold"
          :disabled="props.isDisabled || (authType === 'signup' && !canSubmitSignup)"
          :loading="props.isLoading"
        >
          {{
            props.isLoading
              ? authType === 'login'
                ? 'Logging in...'
                : 'Please wait...'
              : authType === 'login'
                ? 'Login'
                : 'Sign Up'
          }}
        </UButton>

        <div class="flex gap-1">
          <p class="text-sm">
            {{ authType === 'login' ? "Don't have an account?" : 'Already have an account?' }}
          </p>
          <span
            v-if="isDisabled"
            class="text-sm text-violet-700 dark:text-violet-500 opacity-50 cursor-not-allowed"
          >
            {{ authType === 'login' ? 'Sign Up' : 'Login' }}
          </span>
          <NuxtLink
            v-else
            :to="authType === 'login' ? '/signup' : '/login'"
            class="text-sm text-violet-700 dark:text-violet-500 cursor-pointer hover:text-violet-800 dark:hover:text-violet-400 transition-colors"
          >
            {{ authType === 'login' ? 'Sign Up' : 'Login' }}
          </NuxtLink>
        </div>
      </UForm>
    </div>
  </div>
</template>

<style>
::-ms-reveal {
  display: none;
}
</style>