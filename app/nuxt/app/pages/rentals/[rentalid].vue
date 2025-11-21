<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});

const route = useRoute();
const router = useRouter();
const rentalid = route.params.rentalid as string;
const from = route.query.from as string;

const fetchRentalData = async () => {
  if (from === 'rental') {
    // Fetch rental data (user is renting)
    console.log('Fetching rental data for:', rentalid);
  } else if (from === 'lending') {
    // Fetch lending data (user is lending)
    console.log('Fetching lending data for:', rentalid);
  }
}

onMounted(() => {
  fetchRentalData();
});
</script>

<template>
  <div class="min-h-screen w-full pt-4 px-4 md:px-8 lg:px-15">
    <div class="mb-6">
      <button 
        @click="router.back()"
        class="flex items-center gap-2 text-base pt-4 pb-4 hover:text-foreground mb-4 cursor-pointer"
      >
        <Icon name="lucide:arrow-left" class="w-5 h-5" />
        <span>Back to Rentals</span>
      </button>
      
      <h1 class="font-bold text-3xl flex items-center gap-2 mb-1">
        <Icon 
          :name="from === 'rental' ? 'lucide:trending-down' : 'lucide:trending-up'" 
          class="w-8 h-8 text-orange-500" 
        />
        {{ from === 'rental' ? 'Rental Details' : 'Lending Details' }}
      </h1>
      <p class="text-muted">
        {{ from === 'rental' ? 'Viewing your rental' : 'Viewing your lending' }} - ID: {{ rentalid }}
      </p>
    </div>

    <div class="bg-surface rounded-lg border border-base p-6">
      <h2 class="text-xl font-bold mb-4">Rental Information</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <p class="text-sm text-muted">Type</p>
          <p class="font-medium capitalize">{{ from }}</p>
        </div>
        <div>
          <p class="text-sm text-muted">Rental ID</p>
          <p class="font-medium">{{ rentalid }}</p>
        </div>
        <!-- Add more rental/lending details here based on the 'from' parameter -->
      </div>
    </div>
  </div>
</template>