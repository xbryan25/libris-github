<script setup lang="ts">
import type { FormSubmitEvent } from '@nuxt/ui';

const props = defineProps<{
  authType: string;
}>();

const emit = defineEmits<{
  (e: 'onSubmitLogin', email: string, password: string): void;
}>();

const state = reactive({
  emailAddress: '',
  password: '',
  username: '',
  confirmPassword: '',
});

const onSubmit = async (event: FormSubmitEvent<typeof state>) => {
  if (props.authType === 'login') {
    emit('onSubmitLogin', event.data.emailAddress, event.data.password);
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
      <h2 class="text-3xl font-bold">Login</h2>
      <h3>Open the door to endless reading — your next book awaits.</h3>
    </div>

    <UForm
      :validate="(state) => validateAuthForm(state, props.authType)"
      :state="state"
      class="space-y-4"
      @submit="(event) => onSubmit(event)"
    >
      <UFormField label="Email Address" name="emailAddress">
        <UInput v-model="state.emailAddress" class="w-90" />
      </UFormField>

      <UFormField label="Password" name="password">
        <UInput v-model="state.password" type="password" class="w-90" />
      </UFormField>

      <!-- Change to NuxtLink later -->
      <p class="text-sm text-violet-700 dark:text-violet-500 cursor-pointer">
        Forgot your password?
      </p>

      <UButton type="submit" class="w-90 h-9 cursor-pointer justify-center text-lg font-bold"
        >Login</UButton
      >

      <div class="flex gap-1">
        <p class="text-sm">Don't have an account?</p>

        <!-- Change to NuxtLink later -->
        <p class="text-sm text-violet-700 dark:text-violet-500 cursor-pointer">Sign Up</p>
      </div>
    </UForm>
  </div>
</template>
