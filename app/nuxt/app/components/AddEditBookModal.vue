<script setup lang="ts">
const props = defineProps<{
  isOpenAddEditBookModal: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:openAddEditBookModal', value: boolean): void;
}>();

const isOpenAddEditBookModal = computed({
  get: () => props.isOpenAddEditBookModal,
  set: (val: boolean) => {
    emit('update:openAddEditBookModal', val);
  },
});

const value = ref<File[]>([]);

watch(
  () => value.value,
  (newValue: File[]) => {
    if (newValue.length > 5) {
      value.value = newValue.slice(0, 5);
    }
  },
  { deep: true },
);
</script>

<template>
  <UModal v-model:open="isOpenAddEditBookModal">
    <template #header>
      <h2 class="text-3xl font-semibold">Add New Book</h2>
    </template>

    <template #body>
      <UForm class="flex flex-col space-y-4">
        <div class="flex gap-4 w-full">
          <UFormField label="Title" name="title" class="flex-1">
            <UInput />
          </UFormField>

          <UFormField label="Author" name="author" class="flex-1">
            <USelectMenu class="w-full" />
          </UFormField>
        </div>

        <div class="flex gap-4">
          <UFormField label="Genres" name="genre" class="flex-1">
            <USelectMenu
              class="w-full"
              :ui="{
                trailingIcon:
                  'group-data-[state=open]:rotate-180 transition-transform duration-200',
                label: 'text-primary',
              }"
            />
          </UFormField>

          <UFormField label="Condition" name="condition" class="flex-1">
            <USelectMenu
              class="w-full"
              :ui="{
                trailingIcon:
                  'group-data-[state=open]:rotate-180 transition-transform duration-200',
                label: 'text-primary',
              }"
            />
          </UFormField>
        </div>

        <UFormField label="Upload Images" name="uploadImages" class="flex-1">
          <UFileUpload
            v-model="value"
            multiple
            accept="image/*"
            label="Drop your images here"
            description="SVG, PNG, JPG or GIF (max. 2MB). Up to 5 images."
            class="w-full min-h-80"
          />
        </UFormField>

        <UFormField label="Description" name="description" class="flex-1">
          <UTextarea class="w-full min-h-20" :ui="{ base: 'min-h-20 max-h-25' }" />
        </UFormField>

        <div class="flex gap-4">
          <UFormField label="Availability" name="availability" class="flex-1">
            <USelectMenu
              class="w-full"
              :ui="{
                trailingIcon:
                  'group-data-[state=open]:rotate-180 transition-transform duration-200',
                label: 'text-primary',
              }"
            />
          </UFormField>

          <UFormField label="Daily Rent Price" name="dailyRentPrice" class="flex-1">
            <UInput class="w-full" />
          </UFormField>
        </div>

        <div class="flex gap-4 w-full">
          <UFormField label="Security Deposit" name="securityDeposit" class="flex-1">
            <UInput class="w-full" />
          </UFormField>

          <UFormField label="Purchase Price" name="purchasePrice" class="flex-1">
            <UInput class="w-full" />
          </UFormField>
        </div>

        <div class="flex justify-end gap-2 w-full pt-5">
          <UButton
            size="md"
            color="error"
            variant="solid"
            class="cursor-pointer"
            @click="isOpenAddEditBookModal = false"
            >Cancel</UButton
          >
          <UButton size="md" color="primary" variant="solid" type="submit" class="cursor-pointer"
            >Add Book</UButton
          >
        </div>
      </UForm>
    </template>
  </UModal>
</template>