<script setup lang="ts">
import { useBookGenres } from '~/composables/useBookGenres';

interface PriceRange {
  minPrice: number | null;
  maxPrice: number | null;
}

const props = defineProps<{
  headerState: {
    searchValue: string;
    selectedBookGenre: string;
    selectedBookAvailability: string;
    selectedPriceRange: PriceRange;
  };
}>();


const emit = defineEmits<{
  (
    e: 'update:searchValue' | 'update:selectedBookGenre' | 'update:selectedBookAvailability',
    value: string,
  ): void;
   (e: 'update:selectedPriceRange', value: PriceRange): void;
}>();

const searchValue = ref(props.headerState.searchValue);

const bookGenreItems = ref(['All Genres']);
const bookGenreValue = ref(props.headerState.selectedBookGenre);

const bookAvailabilityItems = ref(['All', 'For Rent', 'For Sale', 'Both']);
const bookAvailabilityValue = ref(props.headerState.selectedBookAvailability);

const minPriceValue = ref<number | null>(props.headerState.selectedPriceRange.minPrice ?? null);
const maxPriceValue = ref<number | null>(props.headerState.selectedPriceRange.maxPrice ?? null);

const priceRange = computed<number[]>({
  get: () => [
    minPriceValue.value ?? 0, 
    maxPriceValue.value ?? 1000
  ],
  set: ([min, max]: number[]) => {
    minPriceValue.value = min as number; 
    maxPriceValue.value = max as number;
  }
});

const isFetching = ref(true);
const isPricePopoverOpen = ref(false);

const priceButtonLabel = computed(() => {
  const isFilterActive = 
    (minPriceValue.value !== null && minPriceValue.value !== undefined) || 
    (maxPriceValue.value !== null && maxPriceValue.value !== undefined);
  
  if (isFilterActive) {
    const min = minPriceValue.value?.toString() ?? '0';
    const max = maxPriceValue.value?.toString() ?? 'Max';
    return `Price: ${min} - ${max}`;
  }
  
  return 'Price Range';
});

const loadBookGenreItems = async () => {
  const bookGenres = await useBookGenres();

  isFetching.value = false;

  bookGenreItems.value = ['All Genres', ...bookGenres];
};

watch(
  () => searchValue.value,
  (newSearchValue) => emit('update:searchValue', newSearchValue),
);

watch(
  () => bookGenreValue.value,
  (newBookGenreValue) => emit('update:selectedBookGenre', newBookGenreValue),
);

watch(
  () => bookAvailabilityValue.value,
  (newBookAvailabilityValue) => emit('update:selectedBookAvailability', newBookAvailabilityValue),
);

watch(
  [minPriceValue, maxPriceValue],
  ([newMin, newMax]) => {
    
    const min = (newMin !== null && newMin !== undefined) ? Number(newMin) : null;
    const max = (newMax !== null && newMax !== undefined) ? Number(newMax) : null;

    const finalMin = (min !== null && isFinite(min) && min > 0) ? min : null;
    const finalMax = (max !== null && isFinite(max) && max < 1000) ? max : null;

    emit('update:selectedPriceRange', {
      minPrice: finalMin,
      maxPrice: finalMax,
    });
  },
);

onMounted(async () => {
  await loadBookGenreItems();
});
</script>

<template>
  <div v-if="isFetching" class="mt-5 p-5 bg-surface-hover rounded-lg w-full h-20">
    <div class="flex gap-5">
      <USkeleton class="flex-[4] bg-surface-hover" />
      <USkeleton class="flex-1" />
      <USkeleton class="flex-1" />
    </div>
  </div>

  <div v-else class="mt-5 p-5 bg-surface-hover rounded-lg w-full">
    <div class="flex gap-5">
      <UInput
        v-model="searchValue"
        icon="i-lucide-search"
        size="xl"
        variant="outline"
        placeholder="Search books..."
        class="flex-[4] bg-surface-hover"
      />
      <USelectMenu v-model="bookGenreValue" :items="bookGenreItems" size="xl" class="flex-1" />
      <USelectMenu
        v-model="bookAvailabilityValue"
        :items="bookAvailabilityItems"
        size="xl"
        class="flex-1"
      />
      <UPopover v-model:open="isPricePopoverOpen">
        <UButton
        color="neutral"
        variant="outline"
        size="xl"
        :label="priceButtonLabel"
        :trailing-icon="isPricePopoverOpen ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'"
        class="justify-between"
      />

        <template #content>
          <div class="p-4 flex flex-col gap-4 w-64" @click.stop>
                <label class="font-semibold text-sm">Price Range</label>
                <USlider v-model="priceRange" :min="0" :max="1000" />
                <label class="font-semibold text-sm">Min Price</label>
                <UInput
                  v-model="minPriceValue"
                  type="number"
                  placeholder="No Min"
                  prefix="$"
                  clearable
                />
                <label class="font-semibold text-sm">Max Price</label>
                <UInput
                  v-model="maxPriceValue"
                  type="number"
                  placeholder="No Max"
                  prefix="$"
                  clearable
                />
          </div>
        </template>
    </UPopover>
    </div>
  </div>
</template>
