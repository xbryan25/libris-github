<script setup lang="ts">
import { validateAddEditBook } from '#imports';

import draggable from 'vuedraggable';
import { useUpdateBook } from '~/composables/useUpdateBook';

const props = defineProps<{
  isOpenEditBookModal: boolean;
  bookId: string;
}>();

const emit = defineEmits<{
  (e: 'update:openEditBookModal', value: boolean): void;
  (e: 'editBookSuccess'): void;
}>();

const state = reactive({
  title: '',
  author: '',
  genres: [] as string[],
  originalGenres: [] as string[],
  genresToDelete: [] as string[],
  genresToAdd: [] as string[],
  condition: '',
  bookImages: [] as File[],
  existingBookImageUrls: [] as string[],
  existingBookImageUrlsToDelete: [] as string[],
  allBookOrder: [] as string[],
  description: '',
  availability: '',
  dailyRentPrice: 0,
  securityDeposit: 0,
  purchasePrice: 0,
});

const toast = useToast();

const maxFileSize = 2 * 1024 * 1024; // 2MB
const maxFilesWithExisting = computed(() => 5 - state.existingBookImageUrls.length);

const bookGenreItems = ref<string[]>([]);
const maxGenres = 5;

const conditionItems = ['New', 'Good', 'Used', 'Worn'];
const availabilityItems = ['For Rent', 'For Sale', 'Both'];

const isSubmitting = ref(false);

// To prevent NuxtImg from caching images
const cacheVersion = ref(Date.now());

const { book: bookDetails, fetchBookDetails, loading } = useBookDetails();

const isOpenEditBookModal = computed({
  get: () => props.isOpenEditBookModal,
  set: (val: boolean) => {
    emit('update:openEditBookModal', val);
  },
});

const mergedBookImages = computed({
  get: () => {
    // Build all possible items
    const allItems = [
      ...state.existingBookImageUrls.map((url) => ({
        id: url,
        type: 'existing',
        value: url,
      })),
      ...state.bookImages.map((file) => ({
        id: file.name,
        type: 'new',
        value: file,
      })),
    ];

    // If we already have an order, follow it
    if (state.allBookOrder.length > 0) {
      const ordered = state.allBookOrder
        .map((id) => allItems.find((item) => item.id === id))
        .filter(Boolean) as typeof allItems;

      // Add any new items not yet in order (like newly uploaded ones)
      const missing = allItems.filter((item) => !state.allBookOrder.includes(item.id));
      return [...ordered, ...missing];
    }

    // Otherwise, default to normal order
    return allItems;
  },

  set: (newList) => {
    state.existingBookImageUrls = newList
      .filter((item) => item.type === 'existing')
      .map((item) => item.value as string);

    state.bookImages = newList
      .filter((item) => item.type === 'new')
      .map((item) => item.value as File);

    // Update order
    state.allBookOrder = newList.map((item) => item.id);
  },
});

const resetState = () => {
  Object.assign(state, {
    title: '',
    author: '',
    genres: [],
    originalGenres: [],
    genresToDelete: [],
    genresToAdd: [],
    condition: '',
    bookImages: [],
    existingBookImageUrls: [],
    existingBookImageUrlsToDelete: [],
    allBookOrder: [],
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

const deleteExistingBookImageUrl = (existingBookImageUrl: string) => {
  state.existingBookImageUrlsToDelete.push(existingBookImageUrl);

  state.existingBookImageUrls = state.existingBookImageUrls.filter(
    (bookImageUrl) => bookImageUrl !== existingBookImageUrl,
  );
};

const fetchCurrentBookDetails = async () => {
  try {

    if (props.bookId) {
      await fetchBookDetails(props.bookId);
    } else {
      throw new Error('bookId is required but was not provided.');
    }

    // Assign bookDetails.value to state

    state.title = bookDetails.value?.title as string;
    state.author = bookDetails.value?.author as string;
    state.genres = bookDetails.value?.genres as string[];
    state.originalGenres = bookDetails.value?.genres as string[];
    state.condition = bookDetails.value?.condition
      ? bookDetails.value.condition.charAt(0).toUpperCase() + bookDetails.value.condition.slice(1)
      : '';
    state.existingBookImageUrls = bookDetails.value?.images as string[];
    state.description = bookDetails.value?.description as string;
    state.dailyRentPrice = bookDetails.value?.daily_rent_price as number;
    state.securityDeposit = bookDetails.value?.security_deposit as number;
    state.purchasePrice = bookDetails.value?.purchase_price as number;

    const bookDetailsAvailability = bookDetails.value?.availability as string;

    if (bookDetailsAvailability === 'rent') {
      state.availability = 'For Rent';
    } else if (bookDetailsAvailability === 'purchase') {
      state.availability = 'For Sale';
    } else {
      state.availability = 'Both';
    }

    cacheVersion.value = Date.now();

    console.log(state.existingBookImageUrls);
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

const onSubmit = async () => {
  try {

    isSubmitting.value = true;

    const bookFormData = new FormData();

    state.genresToAdd = state.genres.filter((g) => !state.originalGenres.includes(g));
    state.genresToDelete = state.originalGenres.filter((g) => !state.genres.includes(g));
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

    appendList('genresToAdd', state.genresToAdd);
    appendList('genresToDelete', state.genresToDelete);

    appendList('bookImages', state.bookImages);
    appendList('existingBookImageUrls', state.existingBookImageUrls);
    appendList('existingBookImageUrlsToDelete', state.existingBookImageUrlsToDelete);
    appendList('allBookOrder', state.allBookOrder);

    const data = await useUpdateBook(props.bookId, bookFormData);

    toast.add({
      title: 'Success',
      description: `${data.message}`,
      color: 'success',
    });

    emit('editBookSuccess');

    isOpenEditBookModal.value = false;
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
    description: `Resolve issues to edit the book.`,
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

    if (adjusted.length > maxFilesWithExisting.value) {
      const numOfOverflow = adjusted.length - maxFilesWithExisting.value;

      adjusted = adjusted.slice(0, maxFilesWithExisting.value);

      toast.add({
        title: 'Too Many Images Selected',
        description: `You can only upload up to ${maxFilesWithExisting.value} ${maxFilesWithExisting.value > 1 ? 'images' : 'image'} as there are already ${state.existingBookImageUrls.length} uploaded images. ${numOfOverflow} ${numOfOverflow > 1 ? 'extra images were' : 'extra image was'} ignored.`,
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
  () => props.isOpenEditBookModal,
  async (newValue) => {
    if (!newValue) {
      // e.g. delay reset after modal closes
      setTimeout(() => {
        resetState();
        isSubmitting.value = false;
      }, 300); // delay in ms
    } else {
      loading.value = true;
      await loadBookGenreItems();
      await fetchCurrentBookDetails();
    }
  },
);

onMounted(async () => {
  resetState();
});
</script>

<template>
  <UModal v-model:open="isOpenEditBookModal" :ui="{ content: 'max-w-2xl' }">
    <template #header>
      <h2 class="text-3xl font-semibold">Edit Book</h2>
    </template>

    <template #body>
      <UForm
        v-if="!isSubmitting"
        class="flex flex-col space-y-4"
        :validate="(state) => validateAddEditBook(state, 'edit')"
        :state="state"
        @submit="() => onSubmit()"
        @error="() => onSubmitError()"
      >
        <div class="flex flex-col gap-4 w-full">
          <UFormField label="Title" name="title" class="flex-1">
            <USkeleton v-if="loading" class="w-full h-8" />
            <UInput v-else v-model="state.title" placeholder="Enter book title" class="w-full" />
          </UFormField>

          <UFormField label="Author" name="author" class="flex-1">
            <USkeleton v-if="loading" class="w-full h-8" />
            <UInput v-else v-model="state.author" placeholder="Enter book author" class="w-full" />
          </UFormField>
        </div>

        <div class="flex gap-4">
          <UFormField label="Genres (up to 5)" name="genres" class="flex-1">
            <USkeleton v-if="loading" class="w-full h-8" />
            <USelectMenu
              v-else
              v-model="state.genres"
              :items="bookGenreItems"
              multiple
              placeholder="Select book genres"
              class="w-full max-w-78 overflow-hidden text-ellipsis whitespace-nowrap"
              :ui="{
                trailingIcon:
                  'group-data-[state=open]:rotate-180 transition-transform duration-200',
                label: 'text-primary',
              }"
            />
          </UFormField>

          <UFormField label="Condition" name="condition" class="flex-1">
            <USkeleton v-if="loading" class="w-full h-8" />
            <USelect
              v-else
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


        <UFormField
          v-if="state.existingBookImageUrls.length > 0 || loading"
          label="Existing Images"
          name="existingImages"
          class="flex-1"
        >
          <USkeleton v-if="loading" class="w-full h-80" />
          <div
            v-else
            class="grid grid-cols-3 gap-4 p-4 min-h-80 bg-default border border-default border-dashed rounded-lg content-center"
          >
            <div
              v-for="(image, index) in state.existingBookImageUrls"
              :key="index"
              class="relative"
            >
              <NuxtImg
                :src="`${image}?v=${cacheVersion}`"
                class="rounded-md w-full h-45 object-cover"
              />

              <button
                class="bg-inverted absolute -top-1.5 -right-1.5 rounded-full text-xs cursor-pointer w-5 h-5 border-2 border-bg inline-flex items-center"
                type="button"
                @click="deleteExistingBookImageUrl(image)"
              >
                <Icon name="i-lucide:x" class="size-4 bg-default shrink-0" />
              </button>
            </div>
          </div>
        </UFormField>


        <UFormField label="Upload Images" name="bookImages" class="flex-1">
          <USkeleton v-if="loading" class="w-full h-80" />
          <UFileUpload
            v-else 
            v-model="state.bookImages"
            multiple
            accept="image/png, image/jpeg, image/webp"
            label="Drop your images here"
            description="SVG, PNG, JPG or GIF (max. 2MB). Up to 5 images."
            class="w-full min-h-80"
          />
        </UFormField>

        <UFormField
          v-if="mergedBookImages.length > 1"
          label="Reorder images (drag the image names)"
          name="reorderImages"
          class="flex-1"
        >
          <draggable v-model="mergedBookImages" item-key="id" tag="ul" :animation="300">
            <template #item="{ element }">
              <li class="list-disc list-inside cursor-move px-2 py-1 rounded mb-1 bg-surface-hover">
                <span v-if="element.type === 'existing'">
                  Uploaded image {{ element.value.split('/').pop().at(-1) }}
                </span>
                <span v-else>
                  {{ element.value.name }}
                </span>
              </li>
            </template>
          </draggable>
        </UFormField>

        <UFormField label="Description" name="description" class="flex-1">
          <USkeleton v-if="loading" class="w-full h-20" />
          <UTextarea
            v-else
            v-model="state.description"
            placeholder="Add book description"
            class="w-full min-h-20"
            :ui="{ base: 'min-h-20 max-h-25' }"
          />
        </UFormField>

        <UFormField label="Availability" name="availability" class="flex-1">
          <USkeleton v-if="loading" class="w-full h-8" />
          <USelect
            v-else
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
            @click="isOpenEditBookModal = false"
            >Cancel</UButton
          >
          <UButton
            size="md"
            color="primary"
            variant="solid"
            type="submit"
            class="cursor-pointer"
            :disabled="loading"
            >Edit Book</UButton
          >
        </div>
      </UForm>

      <div v-else class="flex justify-center items-center min-h-[calc(50vh)]">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-accent" />
        <span class="ml-2 text-muted">Editing book...</span>
      </div>
    </template>
  </UModal>
</template>