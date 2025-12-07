<script setup lang="ts">
const props = defineProps<{
  password: string;
  showErrors?: boolean;
}>();

const { validatePassword, getStrengthColor, getStrengthText } = usePasswordValidation();

const validation = computed(() => {
  if (!props.password) {
    return {
      valid: false,
      errors: [],
      strength: 'weak' as const,
      percentage: 0,
    };
  }
  return validatePassword(props.password);
});

const strengthColor = computed(() => {
  return getStrengthColor(validation.value.strength);
});

const strengthText = computed(() => {
  return getStrengthText(validation.value.strength);
});

const barColorClass = computed(() => {
  switch (validation.value.strength) {
    case 'weak':
      return 'bg-red-500';
    case 'medium':
      return 'bg-yellow-500';
    case 'strong':
      return 'bg-green-500';
    default:
      return 'bg-gray-300';
  }
});
</script>

<template>
  <div v-if="password" class="password-strength-meter mt-2">
    <!-- Strength Bar -->
    <div class="flex items-center gap-3 mb-2">
      <div class="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <div
          :class="barColorClass"
          class="h-full transition-all duration-300 ease-out"
          :style="{ width: `${validation.percentage}%` }"
        ></div>
      </div>
      <span
        :class="{
          'text-red-500': validation.strength === 'weak',
          'text-yellow-500': validation.strength === 'medium',
          'text-green-500': validation.strength === 'strong',
        }"
        class="text-sm font-semibold min-w-[60px]"
      >
        {{ strengthText }}
      </span>
    </div>

    <!-- Error Messages -->
    <ul v-if="showErrors && validation.errors.length > 0" class="text-xs text-red-500 space-y-1 mt-2">
      <li v-for="error in validation.errors" :key="error" class="flex items-start gap-1">
        <Icon name="heroicons:x-circle-solid" class="w-4 h-4 flex-shrink-0 mt-0.5" />
        <span>{{ error }}</span>
      </li>
    </ul>

    <!-- Requirements Checklist (Alternative to errors) -->
    <div v-if="!showErrors" class="text-xs space-y-1 mt-2">
      <div class="flex items-center gap-2">
        <Icon
          :name="password.length >= 8 ? 'heroicons:check-circle-solid' : 'heroicons:x-circle-solid'"
          :class="password.length >= 8 ? 'text-green-500' : 'text-gray-400'"
          class="w-4 h-4"
        />
        <span :class="password.length >= 8 ? 'text-green-500' : 'text-gray-500'">
          At least 8 characters
        </span>
      </div>
      <div class="flex items-center gap-2">
        <Icon
          :name="/[A-Z]/.test(password) ? 'heroicons:check-circle-solid' : 'heroicons:x-circle-solid'"
          :class="/[A-Z]/.test(password) ? 'text-green-500' : 'text-gray-400'"
          class="w-4 h-4"
        />
        <span :class="/[A-Z]/.test(password) ? 'text-green-500' : 'text-gray-500'">
          One uppercase letter
        </span>
      </div>
      <div class="flex items-center gap-2">
        <Icon
          :name="/\d/.test(password) ? 'heroicons:check-circle-solid' : 'heroicons:x-circle-solid'"
          :class="/\d/.test(password) ? 'text-green-500' : 'text-gray-400'"
          class="w-4 h-4"
        />
        <span :class="/\d/.test(password) ? 'text-green-500' : 'text-gray-500'">
          One number
        </span>
      </div>
      <div class="flex items-center gap-2">
        <Icon
          :name="/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/\\~`]/.test(password) ? 'heroicons:check-circle-solid' : 'heroicons:x-circle-solid'"
          :class="/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/\\~`]/.test(password) ? 'text-green-500' : 'text-gray-400'"
          class="w-4 h-4"
        />
        <span :class="/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/\\~`]/.test(password) ? 'text-green-500' : 'text-gray-500'">
          One special character
        </span>
      </div>
    </div>
  </div>
</template>