<script setup lang="ts">
import { validateAddEditBook } from '#imports';

import draggable from 'vuedraggable';

const props = defineProps<{
  isOpenAddBookModal: boolean;
  bookId?: string;
}>();

const emit = defineEmits<{
  (e: 'update:openAddBookModal', value: boolean): void;
  (e: 'addBookSuccess'): void;
}>();

const state = reactive({
  title: '',
  author: '',
  genres: [] as string[],
  condition: '',
  bookImages: [] as File[],
  description: '',
  availability: '',
  dailyRentPrice: 0,
  securityDeposit: 0,
  purchasePrice: 0,
});

const toast = useToast();

const maxFileSize = 2 * 1024 * 1024; // 2MB
const maxFiles = 5;

const bookGenreItems = ref<string[]>([]);
const maxGenres = 5;

const conditionItems = ['New', 'Good', 'Used', 'Worn'];
const availabilityItems = ['For Rent', 'For Sale', 'Both'];

const isSubmitting = ref(false);

const resetState = () => {
  Object.assign(state, {
    title: '',
    author: '',
    genres: [],
    condition: '',
    bookImages: [],
    description: '',
    availability: '',
    dailyRentPrice: 0,
    securityDeposit: 0,
    purchasePrice: 0,
  });
};

const loadBookGenreItems = async () => {
  const bookGenres = await useBookGenres();

  bookGenreItems.value = [...bookGenres];
};

const isOpenAddBookModal = computed({
  get: () => props.isOpenAddBookModal,
  set: (val: boolean) => {
    emit('update:openAddBookModal', val);
  },
});

const onSubmit = async () => {
  try {
    isSubmitting.value = true;

    const bookFormData = new FormData();
    bookFormData.append('title', state.title);
    bookFormData.append('author', state.author);
    bookFormData.append('condition', state.condition);
    bookFormData.append('description', state.description);
    bookFormData.append('availability', state.availability);

    if (state.availability === 'For Rent' || state.availability === 'Both') {
      bookFormData.append('dailyRentPrice', state.dailyRentPrice.toString());
      bookFormData.append('securityDeposit', state.securityDeposit.toString());
      bookFormData.append('purchasePrice', (0).toString());
    } else {
      bookFormData.append('dailyRentPrice', (0).toString());
      bookFormData.append('securityDeposit', (0).toString());
      bookFormData.append('purchasePrice', state.purchasePrice.toString());
    }

    const appendList = (key: string, values: any[]) =>
      values.forEach((v) => bookFormData.append(key, v));

    appendList('genres', state.genres);

    appendList('bookImages', state.bookImages);

    const data = await useCreateBook(bookFormData);

    toast.add({
      title: 'Success',
      description: `${data.message}`,
      color: 'success',
    });

    emit('addBookSuccess');

    isOpenAddBookModal.value = false;
  } catch (error) {
    let errorMessage;

    if (error instanceof Error) {
      errorMessage = error.message; // fetch error reason
    }

    if (typeof error === 'object' && error !== null && 'data' in error) {
      errorMessage = (error as any).data.error;
    }

    toast.add({
      title: 'Error',
      description: errorMessage,
      color: 'error',
    });
  }
};

const onSubmitError = () => {
  toast.add({
    title: 'Error with inputs',
    description: `Resolve issues to add a book.`,
    color: 'error',
  });
};

watch(
  () => state.bookImages,
  (newBookImages: File[]) => {
    if (!newBookImages || newBookImages.length === 0) return;

    let adjusted = [...newBookImages];
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
    const filtered: File[] = adjusted.filter((file) => file.size <= maxFileSize);
    const removedCount = adjusted.length - filtered.length;

    if (removedCount > 0) {
      toast.add({
        title: 'File Size Limit Exceeded',
        description: `${removedCount} ${removedCount > 1 ? 'images were' : 'image was'} skipped because they exceed the 2 MB size limit.`,
        color: 'error',
      });

      changed = true;
    }

    // Only update if something changed to avoid infinite recursion
    if (changed) {
      state.bookImages = filtered;
    }
  },
  { deep: true },
);

watch(
  () => state.genres,
  (newGenres: string[]) => {
    if (!newGenres || newGenres.length === 0) return;

    let adjusted: string[] = [...newGenres];
    let changed = false;

    // Limit file count
    if (adjusted.length > maxGenres) {
      adjusted = adjusted.slice(0, maxGenres);

      changed = true;
    }

    // Only update if something changed to avoid infinite recursion
    if (changed) {
      state.genres = adjusted;
    }
  },
  { deep: true },
);

watch(
  () => props.isOpenAddBookModal,
  async (newValue) => {
    if (!newValue) {
      // e.g. delay reset after modal closes
      setTimeout(() => {
        resetState();
        isSubmitting.value = false;
      }, 300); // delay in ms
    }
  },
);

onMounted(async () => {
  await loadBookGenreItems();
  resetState();
});
</script>

<template>
  <UModal v-model:open="isOpenAddBookModal" :ui="{ content: 'max-w-5xl' }">
    <template #header>
      <h2 class="text-3xl font-semibold">Add New Book</h2>
    </template>

    <template #body>
      <UForm
        v-if="!isSubmitting"
        class="flex flex-col space-y-4"
        :validate="(state) => validateAddEditBook(state, 'add')"
        :state="state"
        @submit="() => onSubmit()"
        @error="() => onSubmitError()"
      >
        <div class="flex flex-col gap-4 w-full">
          <UFormField label="Title" name="title" class="flex-1">
            <UInput v-model="state.title" placeholder="Enter book title" class="w-full" />
          </UFormField>

          <UFormField label="Author" name="author" class="flex-1">
            <UInput v-model="state.author" placeholder="Enter book author" class="w-full" />
          </UFormField>
        </div>

        <div class="flex gap-4">
          <UFormField label="Genres (up to 5)" name="genres" class="flex-1">
            <USelectMenu
              v-model="state.genres"
              :items="bookGenreItems"
              multiple
              placeholder="Select book genres"
              class="w-full overflow-hidden text-ellipsis whitespace-nowrap"
              :ui="{
                trailingIcon:
                  'group-data-[state=open]:rotate-180 transition-transform duration-200',
                label: 'text-primary',
              }"
            />
          </UFormField>

          <UFormField label="Condition" name="condition" class="flex-1">
            <USelect
              v-model="state.condition"
              :items="conditionItems"
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

        <UFormField label="Upload Images" name="bookImages" class="flex-1">
          <UFileUpload
            v-model="state.bookImages"
            multiple
            accept="image/png, image/jpeg, image/webp"
            label="Drop your images here"
            description="SVG, PNG, JPG or GIF (max. 2MB). Up to 5 images."
            class="w-full min-h-53"
          />
        </UFormField>

        <UFormField
          v-if="state.bookImages.length > 1"
          label="Reorder images (drag the image names)"
          name="reorderImages"
          class="flex-1"
        >
          <draggable v-model="state.bookImages" item-key="id" tag="ul" :animation="300">
            <template #item="{ element: bookImage }">
              <li class="list-disc list-inside cursor-move px-2 py-1 rounded mb-1 bg-surface-hover">
                {{ bookImage.name }}
              </li>
            </template>
          </draggable>
        </UFormField>

        <UFormField label="Description" name="description" class="flex-1">
          <UTextarea
            v-model="state.description"
            placeholder="Add book description"
            class="w-full min-h-20"
            :ui="{ base: 'min-h-20 max-h-25' }"
          />
        </UFormField>

        <UFormField label="Availability" name="availability" class="flex-1">
          <USelect
            v-model="state.availability"
            :items="availabilityItems"
            placeholder="Select book availability"
            class="w-full"
            :ui="{
              trailingIcon: 'group-data-[state=open]:rotate-180 transition-transform duration-200',
              label: 'text-primary',
            }"
          />
        </UFormField>

        <div class="flex gap-4 w-full">
          <UFormField
            v-if="state.availability === 'For Sale' || state.availability === 'Both'"
            label="Purchase Price"
            name="purchasePrice"
            class="flex-1"
          >
            <UInput v-model="state.purchasePrice" placeholder="Add purchase price" class="w-full" />
          </UFormField>

          <UFormField
            v-if="state.availability === 'For Rent' || state.availability === 'Both'"
            label="Daily Rent Price"
            name="dailyRentPrice"
            class="flex-1"
          >
            <UInput
              v-model="state.dailyRentPrice"
              placeholder="Add daily rent price"
              class="w-full"
            />
          </UFormField>

          <UFormField
            v-if="state.availability === 'For Rent' || state.availability === 'Both'"
            label="Security Deposit"
            name="securityDeposit"
            class="flex-1"
          >
            <UInput
              v-model="state.securityDeposit"
              placeholder="Add security deposit"
              class="w-full"
            />
          </UFormField>
        </div>

        <div class="flex justify-end gap-2 w-full pt-5">
          <UButton
            size="md"
            color="error"
            variant="solid"
            class="cursor-pointer"
            @click="isOpenAddBookModal = false"
            >Cancel</UButton
          >
          <UButton size="md" color="primary" variant="solid" type="submit" class="cursor-pointer"
            >Add Book</UButton
          >
        </div>
      </UForm>

      <div v-else class="flex justify-center items-center min-h-[calc(50vh)]">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-accent" />
        <span class="ml-2 text-muted">Adding book...</span>
      </div>
    </template>
  </UModal>
</template>
