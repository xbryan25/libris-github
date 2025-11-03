<script setup lang="ts">
import type { FormSubmitEvent } from '@nuxt/ui';

const props = defineProps<{
  authType: string;
  isLoading?: boolean;
}>();

const emit = defineEmits<{
  (e: 'onSubmitLogin', email: string, password: string): void;
  (e: 'onSubmitSignup', username: string, email: string, password: string): void;
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
      <h3>{{ authType === 'login' ? 'Open the door to endless reading --- your next book awaits.' : 'Create your account and start your reading journey today.' }}</h3>
    </div>
    <UForm
      :validate="(state) => validateAuthForm(state, props.authType)"
      :state="state"
      class="space-y-4"
      @submit="(event) => onSubmit(event)"
    >
      <UFormField v-if="authType === 'signup'" label="Username" name="username">
        <UInput v-model="state.username" class="w-100 pr-10" :disabled="isLoading" />
      </UFormField>

      <UFormField label="Email Address" name="emailAddress">
        <UInput v-model="state.emailAddress" class="w-100 pr-10" :disabled="isLoading" />
      </UFormField>

      <UFormField label="Password" name="password">
        <div class="relative">
          <UInput 
            v-model="state.password" 
            :type="showPassword ? 'text' : 'password'" 
            class="w-100 pr-10"
            :disabled="isLoading"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute right-23 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            :disabled="isLoading"
          >
            <Icon :name="showPassword ? 'heroicons:eye-slash' : 'heroicons:eye'" class="w-5 h-5" />
          </button>
        </div>
      </UFormField>
      <UFormField v-if="authType === 'signup'" label="Confirm Password" name="confirmPassword">
        <div class="relative">
          <UInput 
            v-model="state.confirmPassword" 
            :type="showConfirmPassword ? 'text' : 'password'" 
            class="w-100 pr-10"
            :disabled="isLoading"
          />
          <button
            type="button"
            @click="showConfirmPassword = !showConfirmPassword"
            class="absolute right-23 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            :disabled="isLoading"
          >
            <Icon :name="showConfirmPassword ? 'heroicons:eye-slash' : 'heroicons:eye'" class="w-5 h-5" />
          </button>
        </div>
      </UFormField>
      <p v-if="authType === 'login'" class="text-sm text-violet-700 dark:text-violet-500 cursor-pointer">
        Forgot your password?
      </p>
      <UButton 
        type="submit" 
        class="w-90 h-9 cursor-pointer justify-center text-lg font-bold"
        :disabled="isLoading"
        :loading="isLoading"
      >
        {{ isLoading ? 'Please wait...' : (authType === 'login' ? 'Login' : 'Sign Up') }}
      </UButton>
      <div class="flex gap-1">
        <p class="text-sm">{{ authType === 'login' ? "Don't have an account?" : "Already have an account?" }}</p>
        <NuxtLink :to="authType === 'login' ? '/signup' : '/login'" class="text-sm text-violet-700 dark:text-violet-500 cursor-pointer">
          {{ authType === 'login' ? 'Sign Up' : 'Login' }}
        </NuxtLink>
      </div>
    </UForm>
  </div>
</template>