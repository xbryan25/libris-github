<script setup lang="ts">
import auth from '~/middleware/auth';
import { useBookDetails } from '~/composables/useBookDetails';
import BookPricing from '~/components/BookPricing.vue';
import { useCreateRental } from '~/composables/useCreateRental';
import { useCreatePurchase } from '~/composables/useCreatePurchase';

definePageMeta({
  middleware: auth,
});

const route = useRoute();
const router = useRouter();
const bookId = route.params.bookId as string;

const { rentalExists, checkRentalExists } = useCreateRental()

const { purchaseExists, checkPurchaseExists } = useCreatePurchase()

const isOpenRentBookModal = ref(false);

const isOpenPurchaseBookModal = ref(false);

const currentWalletBalance = ref(0);
const reservedAmount = ref(0);
const isFetching = ref(true);

onMounted(async () => {
  isFetching.value = true;

  const data = await useCurrentWalletBalance();
  currentWalletBalance.value = data.currentWalletBalance ?? 0;

  isFetching.value = false;
});

onMounted(async () => {
  isFetching.value = true;

  const data = await useReservedAmount();
  reservedAmount.value = data.reserved_amount ?? 0;

  isFetching.value = false;
})

const openRentBookModal = () => {
  isOpenRentBookModal.value = true;
};

const handleRentalSuccess = () => {
  rentalExists.value = true
  isOpenRentBookModal.value = false
}

const openPurchaseBookModal = () => {
  isOpenPurchaseBookModal.value = true;
};

const handlePurchaseSuccess = () => {
  purchaseExists.value = true
  isOpenRentBookModal.value = false
}


const { book, loading, error, fetchBookDetails, availabilityBadges, ownerTrustBadge } =
  useBookDetails();

const currentImageIndex = ref(0);

// Check if book is unavailable (rented or purchased)
const isBookUnavailable = computed(() => {
  if (!book.value) return false;
  return book.value.is_rented || book.value.is_purchased;
});

// Check if book doesn't belong to the collection owner
const isWrongCollection = computed(() => {
  if (!book.value) return false;

  const from = route.query.from as string;
  const collectionOwnerId = route.query.collectionOwnerId as string;

  // If coming from user-collection, verify the book belongs to that user
  if (from === 'user-collection' && collectionOwnerId) {
    return book.value.owner_user_id !== collectionOwnerId;
  }

  return false;
});

// Fetch book details on mount
onMounted(async () => {
  try {
    await fetchBookDetails(bookId);
  } catch (e) {
    console.error('Failed to fetch book details:', e);
  }
});

const setImage = (index: number) => {
  currentImageIndex.value = index;
};

// Action handlers
const handleRent = () => {
  console.log('Rent book:', bookId);
  // Navigate to rent page or open modal
};

const handlePurchase = () => {
  console.log('Purchase book:', bookId);
  // Navigate to purchase page or open modal
};

const goBack = () => {
  const from = route.query.from as string;

  if (from === 'browse') {
    router.push('/browse');
  } else if (from === 'user-collection') {
    // Navigate back to the book owner's collection page
    router.push(`/users/${book.value?.owner_user_id}/collection`);
  } else {
    // Default fallback
    router.push('/browse');
  }
};

const backButtonText = computed(() => {
  const from = route.query.from as string;
  if (from === 'browse') return 'Back to Browse';
  if (from === 'user-collection') return 'Back to Collection';
  return 'Back to Browse';
});

const getBadgeColorClasses = (color: string) => {
  const colors: Record<string, string> = {
    blue: 'bg-blue-600 text-white dark:bg-blue-500',
    red: 'bg-red-600 text-white dark:bg-red-500',
  };
  return colors[color] || colors.gray;
};

onMounted(async () => {
  if (bookId) {
    await checkRentalExists(bookId)
  }
})

</script>

<template>
  <div class="min-h-screen w-full bg-background pt-4 pb-6 px-4 md:px-8 lg:px-15">
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center h-screen">
      <div class="text-center">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-accent" />
        <p class="text-muted mt-2">Loading book details...</p>
      </div>
    </div>

    <!-- Book Unavailable State -->
    <div v-else-if="isBookUnavailable || isWrongCollection" class="flex items-center justify-center h-screen">
      <UCard class="bg-surface border-base max-w-md">
        <div class="text-center p-6">
          <UIcon name="i-heroicons-exclamation-triangle" class="w-16 h-16 text-yellow-500 mx-auto mb-4" />
          <h2 class="text-2xl font-bold text-base mb-2">Book Currently Unavailable</h2>
          <p v-if="isWrongCollection" class="text-muted mb-4">
            This book does not belong to this user's collection.
          </p>
          <p v-else class="text-muted mb-4">
            This book is {{ book?.is_rented ? 'currently rented' : 'purchased' }} and cannot be viewed at this time.
          </p>
          <button
            @click="goBack"
            class="px-6 py-2 bg-accent text-white rounded-lg hover:bg-accent/90 transition cursor-pointer"
          >
            Go Back
          </button>
        </div>
      </UCard>
    </div>

    <!-- Main Content -->
    <div v-else-if="book" class="max-w-7xl pt-3 mx-auto">
      <!-- Back Button -->
      <button
        class="flex items-center gap-2 mb-6 text-base hover:text-accent transition cursor-pointer"
        @click="goBack"
      >
        <UIcon name="i-heroicons-arrow-left" class="text-xl" />
        <span class="font-medium">{{ backButtonText }}</span>
      </button>

      <UCard class="bg-surface border-base">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Left Column - Images -->
          <div>
            <!-- Main Image -->
            <div
              class="relative bg-zinc-200 dark:bg-zinc-800 rounded-lg overflow-hidden mb-4 aspect-[3/4]"
            >
              <img
                v-if="book.images.length > 0"
                :src="book.images[currentImageIndex]"
                :alt="book.title"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-muted">
                <UIcon name="i-heroicons-book-open" class="text-8xl" />
              </div>
            </div>

            <!-- Thumbnail Carousel -->
            <div v-if="book.images.length > 1" class="px-[9%] mb-6">
              <UCarousel
                v-slot="{ item, index }"
                :items="book.images"
                :ui="{
                  item: 'basis-[85px]',
                  container: 'gap-2',
                }"
                arrows
              >
                <button
                  @click="setImage(index)"
                  class="w-[85px] h-[115px] rounded-lg overflow-hidden border-2 transition"
                  :class="
                    index === currentImageIndex
                      ? 'border-accent'
                      : 'border-base hover:border-accent/50'
                  "
                >
                  <img
                    :src="item"
                    :alt="`${book.title} ${index + 1}`"
                    class="w-full h-full object-cover"
                  />
                </button>
              </UCarousel>
            </div>

            <!-- Times Rented & Owner Info -->
            <div class="space-y-4">
              <div class="flex justify-between items-center py-3 px-3 border-y border-base">
                <span class="font-semibold text-base">Times rented:</span>
                <span class="font-bold text-base">{{ book.times_rented || 0 }}</span>
              </div>

              <UCard class="bg-background border-base">
                <h3 class="font-semibold mb-3 text-base">Owner Information</h3>
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="relative">
                      <img
                        v-if="book.owner_profile_picture"
                        :src="book.owner_profile_picture"
                        :alt="book.owner_username"
                        class="w-10 h-10 rounded-full object-cover"
                      />
                      <div
                        v-else
                        class="w-10 h-10 rounded-full bg-surface flex items-center justify-center"
                      >
                        <Icon name="heroicons:user-solid" class="w-7 h-7 text-muted" />
                      </div>
                    </div>
                    <div>
                      <NuxtLink
                        :to="`/users/${book.owner_user_id}`"
                        class="font-medium text-base px-1 py-1 hover:text-accent rounded-md hover:bg-surface-hover transition cursor-pointer"
                      >
                        {{ book.owner_username }}
                      </NuxtLink>
                    </div>
                  </div>
                  <div class="flex flex-col items-end">
                    <span class="text-2xl font-bold text-base">{{ book.owner_trust_score }}</span>
                    <span
                      class="text-xs px-2 py-1 rounded-full font-medium text-white"
                      :class="[
                        ownerTrustBadge.color,
                        ownerTrustBadge.text === 'Poor' ? 'border border-white' : '',
                      ]"
                    >
                      {{ ownerTrustBadge.text }}
                    </span>
                  </div>
                </div>
              </UCard>
            </div>
          </div>

          <!-- Right Column - Details -->
          <div class="flex flex-col">
            <div class="flex-grow">
              <h1 class="text-[42px] font-bold text-base mb-2">
                {{ book.title.length > 130 ? book.title.substring(0, 130) + '...' : book.title }}
              </h1>
              <p class="text-muted mb-4">by {{ book.author }}</p>

              <!-- Badges -->
              <div class="flex flex-wrap gap-2 mb-6">
                <span
                  v-for="(genre, idx) in book.genres"
                  :key="idx"
                  class="px-3 py-1 bg-surface border border-base rounded-full text-sm text-base"
                >
                  {{ genre }}
                </span>
                <span
                  class="px-3 py-1 bg-yellow-400 text-zinc-900 rounded-full text-sm font-medium capitalize"
                >
                  {{ book.condition }}
                </span>
                <span
                  v-for="(badge, idx) in availabilityBadges"
                  :key="`avail-${idx}`"
                  class="px-3 py-1 rounded-full text-sm font-medium"
                  :class="getBadgeColorClasses(badge.color)"
                >
                  {{ badge.label }}
                </span>
              </div>

              <!-- Description -->
              <div class="mb-6">
                <h2 class="font-semibold text-lg mb-2 text-base">Description</h2>
                <p class="text-base text-justify leading-relaxed">{{ book.description }}</p>
              </div>
            </div>

            <!-- Pricing Options -->
            <div class="mt-auto">
              <BookPricing
                :availability="book.availability"
                :daily-rent-price="book.daily_rent_price"
                :security-deposit="book.security_deposit"
                :purchase-price="book.purchase_price"
                :book-id="bookId ?? ''"
                :rental-exists="rentalExists"
                :purchase-exists="purchaseExists"
                @rent="openRentBookModal"
                @purchase="openPurchaseBookModal"
              />
            </div>
          </div>
        </div>
      </UCard>
    </div>
    <RentBookModal
      :is-open-rent-book-modal="isOpenRentBookModal"
      :book-id="bookId ?? ''"
      :book-title="book?.title"
      :daily-rent-price="book?.daily_rent_price"
      :security-deposit="book?.security_deposit"
      :rental-exists="rentalExists"
      :current-wallet-balance="currentWalletBalance"
      :reserved-amount="reservedAmount"
      @update:openRentBookModal="isOpenRentBookModal = $event"
      @rental-success="handleRentalSuccess"
    />
    <PurchaseBookModal
      :is-open-purchase-book-modal="isOpenPurchaseBookModal"
      :book-id="bookId ?? ''"
      :book-title="book?.title"
      :book-author="book?.author"
      :purchase-price="book?.purchase_price"
      :current-wallet-balance="currentWalletBalance"
      :purchase-exists="purchaseExists"
      :reserved_amount="reservedAmount"
      @update:openPurchaseBookModal="isOpenPurchaseBookModal = $event"
      @purchase-success="handlePurchaseSuccess"
    />
  </div>
</template>