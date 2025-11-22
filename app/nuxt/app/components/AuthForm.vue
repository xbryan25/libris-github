<script setup lang="ts">
import type { FormSubmitEvent } from '@nuxt/ui';

const props = defineProps<{
  authType: string;
  isLoading?: boolean;
}>();

const emit = defineEmits<{
  (e: 'onSubmitLogin', email: string, password: string): void;
  (e: 'onSubmitSignup', username: string, email: string, password: string): void;
  (e: 'onSubmitGmailLogin'): void;
}>();

const state = reactive({
  emailAddress: '',
  password: '',
  username: '',
  confirmPassword: '',
});

const showPassword = ref(false);
const showConfirmPassword = ref(false);

const onSubmit = async (event: FormSubmitEvent<typeof state>) => {
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

    <UButton
      v-if="authType === 'login'"
      label="Login with Google"
      @click="emit('onSubmitGmailLogin')"
    />

    <UForm
      :validate="(state) => validateAuthForm(state, props.authType)"
      :state="state"
      class="space-y-4"
      @submit="(event) => onSubmit(event)"
    >
      <UFormField v-if="authType === 'signup'" label="Username" name="username">
        <UInput v-model="state.username" class="w-100" :disabled="isLoading" />
      </UFormField>

      <UFormField label="Email Address" name="emailAddress">
        <UInput v-model="state.emailAddress" class="w-100" :disabled="isLoading" />
      </UFormField>

      <UFormField label="Password" name="password">
        <UInput
          v-model="state.password"
          :type="showPassword ? 'text' : 'password'"
          class="w-100"
          :disabled="isLoading"
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
              :disabled="isLoading"
              @click="showPassword = !showPassword"
            />
          </template>
        </UInput>
      </UFormField>

      <UFormField v-if="authType === 'signup'" label="Confirm Password" name="confirmPassword">
        <UInput
          v-model="state.confirmPassword"
          :type="showConfirmPassword ? 'text' : 'password'"
          class="w-100"
          :disabled="isLoading"
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
              :disabled="isLoading"
              @click="showConfirmPassword = !showConfirmPassword"
            />
          </template>
        </UInput>
      </UFormField>

      <div v-if="authType === 'login'" class="w-full">
        <p class="text-sm inline-block text-violet-700 dark:text-violet-500 cursor-pointer">
          Forgot your password?
        </p>
      </div>

      <UButton
        type="submit"
        class="w-100 h-9 cursor-pointer justify-center text-lg font-bold"
        :disabled="isLoading"
        :loading="isLoading"
      >
        {{
          isLoading
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
        <NuxtLink
          :to="authType === 'login' ? '/signup' : '/login'"
          class="text-sm text-violet-700 dark:text-violet-500 cursor-pointer"
        >
          {{ authType === 'login' ? 'Sign Up' : 'Login' }}
        </NuxtLink>
      </div>
    </UForm>
  </div>
</template>

<style>
::-ms-reveal {
  display: none;
}
</style>
