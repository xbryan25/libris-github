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

const toast = useToast();

const maxFileSize = 2 * 1024 * 1024; // 2MB
const maxFiles = 5;

const value = ref<File[]>([]);

watch(
  () => value.value,
  (newValue: File[]) => {
 if (!newValue || newValue.length === 0) return;

    let adjusted = [...newValue];
    let changed = false;

    // Limit file count
    if (adjusted.length > maxFiles) {
      const numOfOverflow = adjusted.length - maxFiles;

      adjusted = adjusted.slice(0, maxFiles);

      toast.add({
        title: 'Too Many Images Selected',
        description: `You can only upload up to ${maxFiles} images. ${numOfOverflow} ${numOfOverflow > 1 ? 'extra files were' : 'extra file was'} ignored.`,
        color: 'error',
      });

      changed = true;
    }

    // Filter large files
    const filtered = adjusted.filter((file) => file.size <= maxFileSize);
    const removedCount = adjusted.length - filtered.length;

    if (removedCount > 0) {
      toast.add({
        title: 'File Size Limit Exceeded',
        description: `${removedCount} ${removedCount > 1 ? 'images were' : 'image was'} skipped because they exceed the 2 MB size limit.`,
        color: 'error',
      });

      changed = true;
    }

    // ✅ Only update if something changed to avoid infinite recursion
    if (changed) {
      value.value = filtered;
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
            <UInput placeholder="Enter book title" />
          </UFormField>

          <UFormField label="Author" name="author" class="flex-1">
            <UInput placeholder="Enter book author" />
          </UFormField>
        </div>

        <div class="flex gap-4">
          <UFormField label="Genres" name="genre" class="flex-1">
            <USelectMenu
              placeholder="Select book genres"
              multiple
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
              placeholder="Select book condition"
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
            accept="image/png, image/jpeg, image/webp"
            label="Drop your images here"
            description="SVG, PNG, JPG or GIF (max. 2MB). Up to 5 images."
            class="w-full min-h-80"
          />
        </UFormField>

        <UFormField label="Description" name="description" class="flex-1">
        <UTextarea
            placeholder="Add book description"
            class="w-full min-h-20"
            :ui="{ base: 'min-h-20 max-h-25' }"
          />
        </UFormField>

        <div class="flex gap-4">
          <UFormField label="Availability" name="availability" class="flex-1">
            <USelectMenu
              placeholder="Select book availability"
              class="w-full"
              :ui="{
                trailingIcon:
                  'group-data-[state=open]:rotate-180 transition-transform duration-200',
                label: 'text-primary',
              }"
            />
          </UFormField>

          <UFormField label="Daily Rent Price" name="dailyRentPrice" class="flex-1">
            <UInput placeholder="Add daily rent price" class="w-full" />
          </UFormField>
        </div>

        <div class="flex gap-4 w-full">
          <UFormField label="Security Deposit" name="securityDeposit" class="flex-1">
            <UInput placeholder="Add security deposit" class="w-full" />
          </UFormField>

          <UFormField label="Purchase Price" name="purchasePrice" class="flex-1">
            <UInput placeholder="Add purchase price" class="w-full" />
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