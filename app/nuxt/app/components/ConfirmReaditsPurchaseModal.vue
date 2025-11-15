<script setup lang="ts">
import { capitalizeWords } from '#imports';

const props = defineProps<{
  isOpenConfirmPurchaseModal: boolean;
  selectedPack: string;
}>();

const emit = defineEmits<{
  (e: 'update:openConfirmPurchaseModal', value: boolean): void;
}>();

const isOpenConfirmPurchaseModal = computed({
  get: () => props.isOpenConfirmPurchaseModal,
  set: (val: boolean) => {
    emit('update:openConfirmPurchaseModal', val);
  },
});

const packToReaditsMap: Record<string, [number, number]> = {
  starter: [100, 200],
  popular: [150, 600],
  pro: [350, 1000],
  ultra: [750, 5000],
};

const isModalConfirmClicked = ref(false);

const toast = useToast();

const onSubmit = () => {
  isModalConfirmClicked.value = true;

  toast.add({
    title: 'Transaction successful',
    description: `${packToReaditsMap[props.selectedPack]?.[0]} Readits has been sent to your account.`,
    color: 'success',
    icon: 'fluent:book-coins-20-regular',
    ui: { icon: 'w-16 h-16' },
  });

  isOpenConfirmPurchaseModal.value = false;
  isModalConfirmClicked.value = false;
};
</script>

<template>
  <UModal v-model:open="isOpenConfirmPurchaseModal">
    <template #header>
      <h2 class="text-3xl font-semibold">Confirm purchase?</h2>
    </template>

    <template #body>
      <div class="flex flex-col gap-2 mx-3">
        <h2 class="font-bold text-2xl mb-1">Purchase Details</h2>
        <div class="flex">
          <p class="flex-1 text-lg">Pack Type:</p>
          <p class="text-lg">{{ capitalizeWords(props.selectedPack) }} Pack</p>
        </div>
        <div class="flex">
          <p class="flex-1 text-lg">You will gain:</p>
          <div class="flex items-center gap-1">
            <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent" />

            <span class="text-lg font-semibold text-accent">{{
              packToReaditsMap[props.selectedPack]?.[0]
            }}</span>
          </div>
        </div>

        <USeparator color="primary" size="sm" class="w-full" />

        <div class="flex">
          <p class="flex-1 text-lg font-semibold">Total Price:</p>
          <p class="text-lg font-semibold">₱{{ packToReaditsMap[props.selectedPack]?.[1] }}</p>
        </div>

        <div class="flex justify-end gap-2 mt-3">
          <UButton color="error" class="cursor-pointer" @click="isOpenConfirmPurchaseModal = false"
            >Cancel</UButton
          >
          <UButton
            class="cursor-pointer"
            :disabled="isModalConfirmClicked"
            :loading="isModalConfirmClicked"
            @click="onSubmit()"
            >Confirm</UButton
          >
        </div>
      </div>
    </template>
  </UModal>
</template>
