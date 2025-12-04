<script setup lang="ts">
import { useBookGenres } from '~/composables/useBookGenres';

interface PriceRange {
  minPrice: number | null;
  maxPrice: number | null;
}

const kmRadiusOptions = [
  { label: 'Any Distance', value: null },
  { label: '2 km', value: 2 },
  { label: '5 km', value: 5 },
  { label: '10 km', value: 10 },
  { label: '25 km', value: 25 },
  { label: '50 km', value: 50 },
];

const props = defineProps<{
  headerState: {
    searchValue: string;
    selectedBookGenre: string;
    selectedBookAvailability: string;
    selectedPriceRange: PriceRange;
    kmRadius: number | null;
  };
  isLibraryMode?: boolean;
}>();


const emit = defineEmits<{
  (
    e: 'update:searchValue' | 'update:selectedBookGenre' | 'update:selectedBookAvailability',
    value: string,
  ): void;
   (e: 'update:selectedPriceRange', value: PriceRange): void;
   (e: 'update:kmRadius', value: number | null): void;
}>();


const searchValue = ref(props.headerState.searchValue);

const kmRadiusItems = ref(kmRadiusOptions);
const kmRadiusValue = ref(
  kmRadiusOptions.find(item => item.value === props.headerState.kmRadius) || kmRadiusOptions[0]
);

const bookGenreItems = ref(['All Genres']);
const bookGenreValue = ref(props.headerState.selectedBookGenre);

const bookAvailabilityItems = ref(['All', 'For Rent', 'For Sale', 'Both']);
const bookAvailabilityValue = ref(props.headerState.selectedBookAvailability);

const _minPrice = ref<number | null>(props.headerState.selectedPriceRange.minPrice ?? null);
const _maxPrice = ref<number | null>(props.headerState.selectedPriceRange.maxPrice ?? null);

const minPriceValue = computed({
  get: () => _minPrice.value,
  set: (val: number | string | null) => {
    const num = Number(val);

    if (val === '' || val === null || isNaN(num)) {
      _minPrice.value = null;
      return;
    }

    _minPrice.value = num;
  }
});

const maxPriceValue = computed({
  get: () => _maxPrice.value,
  set: (val: number | string | null) => {
    const num = Number(val);

    if (val === '' || val === null || isNaN(num)) {
      _maxPrice.value = null;
      return;
    }

    _maxPrice.value = num;
  }
});

const priceRange = computed<number[]>({
  get: () => [
    (_minPrice.value && _minPrice.value > 0) ? _minPrice.value : 1,
    (_maxPrice.value && _maxPrice.value > 0) ? _maxPrice.value : 1000
  ],
  set: (val: number[]) => {
    const min = val[0];
    const max = val[1];

    minPriceValue.value = (typeof min === 'number' && min > 1) ? min : null;
    maxPriceValue.value = (typeof max === 'number' && max < 1000) ? max : null;
  }
});

const priceErrorMessage = ref('');

const isFetching = ref(true);
const isPricePopoverOpen = ref(false);

const priceButtonColor = computed(() => {
  return priceErrorMessage.value ? 'error' : 'neutral'
})

const priceButtonLabel = computed(() => {
  const isFilterActive = 
    (minPriceValue.value !== null && minPriceValue.value !== undefined) || 
    (maxPriceValue.value !== null && maxPriceValue.value !== undefined);

  if (isFilterActive) {
    const min = minPriceValue.value?.toString() ?? '1';
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
  [_minPrice, _maxPrice],
  ([newMin, newMax]) => {
    if (isFetching.value) return;
    priceErrorMessage.value = ''; 

    if ((newMin !== null && newMin <= 0) || (newMax !== null && newMax <= 0)) {
        priceErrorMessage.value = "Prices must be greater than 0.";
        
        emit('update:selectedPriceRange', {
            minPrice: (newMin && newMin > 0) ? newMin : 1,
            maxPrice: (newMax && newMax > 0) ? newMax : null,
        });
        return;
    }

    if (newMin !== null && newMax !== null && newMin >= newMax) {
        priceErrorMessage.value = "Min price must be less than Max price.";
        emit('update:selectedPriceRange', {
            minPrice: 1,
            maxPrice: null,
        });
        return;
    }

    emit('update:selectedPriceRange', {
      minPrice: newMin ?? 1,
      maxPrice: newMax,
    });
  },
);

watch(
  () => kmRadiusValue.value,
  (newItem) => {
    if (!newItem) return; 
    emit('update:kmRadius', newItem.value)
  }
)

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
          :color="priceButtonColor"
          variant="outline"
          size="xl"
          :label="priceButtonLabel"
          :trailing-icon="isPricePopoverOpen ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'"
          class="justify-between"
        />

        <template #content>
          <div class="p-4 flex flex-col gap-4 w-64" @click.stop>
                <label class="font-semibold text-sm">Price Range</label>
                <p v-if="priceErrorMessage" class="text-red-500 text-xs font-medium">
                    {{ priceErrorMessage }}
                </p>
                <USlider v-model="priceRange" :min="1" :max="1000" />
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
    <USelectMenu
      v-if="!isLibraryMode"
      v-model="kmRadiusValue"
      :items="kmRadiusItems"
      size="xl"
      class="flex-1"
    />
    </div>
  </div>
</template>
