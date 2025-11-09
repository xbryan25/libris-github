<script setup lang="ts">
const props = defineProps<{
  isOpenDeleteBookModal: boolean;
  bookId: string;
  bookTitle: string;
}>();

const emit = defineEmits<{
  (e: 'update:openDeleteBookModal', value: boolean): void;
  (e: 'deleteBookSuccess'): void;
}>();

const toast = useToast();

const isSubmitting = ref(false);

const isOpenDeleteBookModal = computed({
  get: () => props.isOpenDeleteBookModal,
  set: (val: boolean) => {
    emit('update:openDeleteBookModal', val);
  },
});

const onSubmit = async () => {
  try {
    isSubmitting.value = true;

    const data = await useDeleteBook(props.bookId, props.bookTitle);

    toast.add({
      title: 'Success',
      description: `${data.message}`,
      color: 'success',
    });

    emit('deleteBookSuccess');

    isOpenDeleteBookModal.value = false;
  } catch {
    toast.add({
      title: 'Error',
      description: `There was an error in deleting '${state.title}'. Try again.`,
      color: 'error',
    });
  }
};

watch(
  () => props.isOpenDeleteBookModal,
  async (newValue) => {
    if (!newValue) {
      // e.g. delay reset after modal closes
      setTimeout(() => {
        isSubmitting.value = false;
      }, 300); // delay in ms
    }
  },
);
</script>

<template>
  <UModal v-model:open="isOpenDeleteBookModal" :ui="{ content: 'max-w-xl' }">
    <template #header>
      <h2 class="text-3xl font-semibold">Delete a book</h2>
    </template>

    <template #body>
      <div v-if="!isSubmitting" class="flex flex-col justify-center min-h-25">
        <div class="flex justify-center w-full">
          <UTooltip :text="props.bookTitle">
            <h2 class="truncate w-full text-center text-lg">
              Confirm deletion of {{ props.bookTitle }}?
            </h2>
          </UTooltip>
        </div>

        <div class="flex justify-center gap-2 w-full pt-5">
          <UButton
            size="md"
            color="error"
            variant="solid"
            class="cursor-pointer"
            @click="isOpenDeleteBookModal = false"
            >Cancel</UButton
          >
          <UButton
            size="md"
            color="primary"
            variant="solid"
            type="submit"
            class="cursor-pointer"
            @click="onSubmit"
            >Proceed</UButton
          >
        </div>
      </div>

      <div v-else class="flex justify-center items-center min-h-25">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-accent" />
        <span class="ml-2 text-muted">Deleting book...</span>
      </div>
    </template>
  </UModal>
</template>
