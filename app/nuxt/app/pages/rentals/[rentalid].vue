<script setup lang="ts">
import auth from '~/middleware/auth';
import { useUserRentals, type Rental } from '~/composables/useUserRentals';
import { useUserLendings, type Lending } from '~/composables/useUserLendings';

definePageMeta({
  middleware: auth,
});

const route = useRoute();
const router = useRouter();
const rentalid = route.params.rentalid as string;
const from = route.query.from as string;

const { rentals, fetchUserRentals } = useUserRentals();
const { lendings, fetchUserLendings } = useUserLendings();

const currentItem = ref<Rental | Lending | null>(null);
const loading = ref(true);

const fetchRentalData = async () => {
  loading.value = true;
  try {
    if (from === 'rental') {
      await fetchUserRentals();
      currentItem.value = rentals.value.find(r => r.rental_id === rentalid) || null;
    } else if (from === 'lending') {
      await fetchUserLendings();
      currentItem.value = lendings.value.find(l => l.rental_id === rentalid) || null;
    }
  } catch (error) {
    console.error('Error fetching rental data:', error);
  } finally {
    loading.value = false;
  }
}

const getStatusBadge = (status: string) => {
  const statusConfig: Record<string, { label: string; color: string }> = {
    pending: { label: 'Pending Approval', color: 'bg-yellow-500' },
    approved: { label: 'Confirmed', color: 'bg-blue-500' },
    awaiting_pickup_confirmation: { label: 'Pickup Arranged', color: 'bg-orange-500' },
    ongoing: { label: 'Book Received', color: 'bg-purple-500' },
    awaiting_return_confirmation: { label: 'Return Initiated', color: 'bg-indigo-500' },
    completed: { label: 'Return Complete', color: 'bg-green-500' }
  }
  
  return statusConfig[status] || { label: status, color: 'bg-gray-500' }
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

const formatDateTime = (dateString: string) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

const handleCancelRequest = () => {
  // Add cancel request logic here
  console.log('Cancel request for:', rentalid);
}

const getStepperItems = (status: string) => {
  if (from === 'rental') {
    return [
      {
        title: 'Requested',
        description: 'Rental request sent',
        icon: 'i-lucide-send'
      },
      {
        title: 'Confirmed',
        description: 'Owner approved request',
        icon: 'i-lucide-check-circle'
      },
      {
        title: 'Pickup',
        description: 'Ready for pickup',
        icon: 'i-lucide-package'
      },
      {
        title: 'Renting',
        description: 'Currently renting',
        icon: 'i-lucide-book-open'
      },
      {
        title: 'Return',
        description: 'Ready for return',
        icon: 'i-lucide-package-check'
      },
      {
        title: 'Completed',
        description: 'Rental finished',
        icon: 'i-lucide-circle-check'
      }
    ]
  } else {
    return [
      {
        title: 'Pending',
        description: 'Rental request received',
        icon: 'i-lucide-send'
      },
      {
        title: 'Confirmed',
        description: 'Approved request',
        icon: 'i-lucide-check-circle'
      },
      {
        title: 'Delivered',
        description: 'Book Delivered',
        icon: 'i-lucide-package'
      },
      {
        title: 'Active',
        description: 'Currently renting',
        icon: 'i-lucide-book-open'
      },
      {
        title: 'Pickup',
        description: 'Ready for return pickup',
        icon: 'i-lucide-package-check'
      },
      {
        title: 'Completed',
        description: 'Rental finished',
        icon: 'i-lucide-circle-check'
      }
    ]
  }
}

const getCurrentStep = (status: string) => {
  const statusOrder = ['pending', 'approved', 'awaiting_pickup_confirmation', 'ongoing', 'awaiting_return_confirmation', 'completed']
  return statusOrder.indexOf(status)
}

const isWithinOneHourOfMeetup = computed(() => {
  // Only check if status is 'approved'
  if (currentItem.value?.rent_status !== 'approved') {
    return false;
  }
  
  if (!currentItem.value?.meetup_date || !currentItem.value?.meetup_time) {
    return false;
  }
  
  // Combine meetup_date and meetup_time into a full datetime
  const meetupDateTime = new Date(`${currentItem.value.meetup_date} ${currentItem.value.meetup_time}`);
  const now = new Date();
  const oneHourBeforeMeetup = new Date(meetupDateTime.getTime() - 60 * 60 * 1000);
  
  // Check if current time is within 1 hour before meetup and not past the meetup time
  return now >= oneHourBeforeMeetup && now <= meetupDateTime;
})

onMounted(() => {
  fetchRentalData();
});
</script>

<template>
  <div class="min-h-screen w-full pt-4 pb-6 px-4 md:px-8 lg:px-15">
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

    <!-- Loading State -->
    <div v-if="loading" class="bg-surface rounded-lg border border-base p-12">
      <div class="flex justify-center items-center">
        <div class="text-center">
          <Icon name="lucide:loader-2" class="w-12 h-12 text-muted mx-auto animate-spin" />
          <p class="text-muted mt-4 text-lg">Loading details...</p>
        </div>
      </div>
    </div>

    <!-- Not Found State -->
    <div v-else-if="!currentItem" class="bg-surface rounded-lg border border-base p-12">
      <div class="flex justify-center items-center">
        <div class="text-center">
          <Icon name="lucide:alert-circle" class="w-16 h-16 text-red-500 mx-auto" />
          <p class="text-red-500 mt-4 text-lg">Rental not found</p>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div v-else class="space-y-6">
      <!-- Book Information Card -->
      <div class="bg-surface rounded-lg border border-base p-6">
        <div class="flex gap-6">
          <img 
            :src="currentItem.image" 
            :alt="currentItem.title"
            class="w-32 h-48 object-cover rounded-lg"
          />
          <div class="flex-1">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h2 class="text-2xl font-bold mb-1">{{ currentItem.title }}</h2>
                <p class="text-muted">by {{ currentItem.author }}</p>
              </div>
              <span 
                :class="[getStatusBadge(currentItem.rent_status).color, 'text-white px-4 py-2 rounded-full text-sm font-medium']"
              >
                {{ getStatusBadge(currentItem.rent_status).label }}
              </span>
            </div>

            <div class="grid grid-cols-2 gap-4 mt-6">
              <div>
                <p class="text-sm text-muted">{{ from === 'rental' ? 'Renting from' : 'Lending to' }}</p>
                <p class="font-medium text-lg">{{ from === 'rental' ? (currentItem as Rental).from : (currentItem as Lending).to }}</p>
              </div>
              <div>
                <p class="text-sm text-muted">Duration</p>
                <p class="font-medium text-lg">{{ currentItem.rental_duration_days }} days</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress Stepper Card - Show only if status is not pending -->
      <div v-if="currentItem.rent_status !== 'pending'" class="bg-surface rounded-lg border border-base p-6">
        <UStepper 
          disabled
          :items="getStepperItems(currentItem.rent_status)" 
          :model-value="getCurrentStep(currentItem.rent_status)"
        />
      </div>

      <!-- Rental Details Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Dates Card -->
        <div class="bg-surface rounded-lg border border-base p-6">
          <h3 class="text-xl font-bold mb-4 flex items-center gap-2">
            <Icon name="lucide:calendar" class="w-5 h-5" />
            Important Dates
          </h3>
          <div class="space-y-4">
            <div v-if="currentItem.rent_status === 'pending'">
              <p class="text-sm text-muted">Start Date</p>
              <p class="font-medium">Pending</p>
            </div>
            <div v-else>
              <p class="text-sm text-muted">Start Date</p>
              <p class="font-medium">{{ formatDate(currentItem.rent_start_date) }}</p>
            </div>
            
            <div v-if="currentItem.rent_status === 'pending'">
              <p class="text-sm text-muted">End Date</p>
              <p class="font-medium">in {{ currentItem.rental_duration_days }} days</p>
            </div>
            <div v-else>
              <p class="text-sm text-muted">End Date</p>
              <p class="font-medium">{{ formatDate(currentItem.rent_end_date) }}</p>
            </div>

            <div v-if="currentItem.reserved_at">
              <p class="text-sm text-muted">Reserved At</p>
              <p class="font-medium">{{ formatDateTime(currentItem.reserved_at) }}</p>
            </div>

            <div v-if="currentItem.reservation_expires_at && currentItem.rent_status === 'pending'">
              <p class="text-sm text-muted">Reservation Expires</p>
              <p class="font-medium text-red-600">{{ formatDateTime(currentItem.reservation_expires_at) }}</p>
            </div>
          </div>
        </div>

        <!-- Meetup Information Card -->
        <div class="bg-surface rounded-lg border border-base p-6">
          <h3 class="text-xl font-bold mb-4 flex items-center gap-2">
            <Icon name="lucide:map-pin" class="w-5 h-5" />
            Meetup Information
          </h3>
          <div class="space-y-4">
            <div v-if="currentItem.meetup_date">
              <p class="text-sm text-muted">Initial Meetup Date</p>
              <p class="font-medium">{{ formatDate(currentItem.meetup_date) }}</p>
            </div>

            <div>
              <p class="text-sm text-muted">Meetup Location</p>
              <p class="font-medium">{{ currentItem.meetup_location || 'Not set' }}</p>
            </div>

            <div v-if="currentItem.meetup_time">
              <p class="text-sm text-muted">Meetup Time</p>
              <p class="font-medium">{{ currentItem.meetup_time }}</p>
            </div>

            <div v-if="currentItem.meetup_time_window">
              <p class="text-sm text-muted">Time Window</p>
              <p class="font-medium">{{ currentItem.meetup_time_window }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Cost Information Card - Compact Version -->
      <div class="bg-surface rounded-lg border border-base p-5">
        <h3 class="text-lg font-bold mb-3 flex items-center gap-2">
          <Icon name="fluent:book-coins-20-regular" class="w-5 h-5" />
          Cost Details
        </h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p class="text-xs text-muted mb-1">Security Deposit</p>
            <div class="flex items-center gap-1">
              <Icon name="fluent:book-coins-20-regular" class="w-4 h-4 text-accent" />
              <span class="font-bold text-lg text-accent">15</span>
            </div>
          </div>
          
          <div>
            <p class="text-xs text-muted mb-1">Daily Rate</p>
            <div class="flex items-center gap-1">
              <Icon name="fluent:book-coins-20-regular" class="w-4 h-4 text-accent" />
              <span class="font-bold text-lg text-accent">3</span>
            </div>
          </div>

          <div>
            <p class="text-xs text-muted mb-1">Total Cost</p>
            <div class="flex items-center gap-1">
              <span class="text-sm font-bold">{{ from === 'rental' ? '-' : '+' }}</span>
              <Icon name="fluent:book-coins-20-regular" class="w-4 h-4 text-accent" />
              <span class="font-bold text-lg text-accent">{{ currentItem.cost }}</span>
            </div>
          </div>

          <div>
            <p class="text-xs text-muted mb-1">Payment Status</p>
            <p class="font-medium text-sm" :class="currentItem.all_fees_captured ? 'text-green-600' : 'text-yellow-600'">
              {{ currentItem.all_fees_captured ? 'Captured' : 'Pending' }}
            </p>
          </div>
        </div>
      </div>

      <!-- Handoff Confirmation Card - Only show if status is approved -->
      <div v-if="currentItem.rent_status === 'approved'">
        <!-- Warning Message - Show when NOT within 1 hour -->
        <div v-if="!isWithinOneHourOfMeetup" class="bg-blue-50 border border-blue-200 rounded-lg p-5">
          <div class="flex items-start gap-3">
            <Icon name="lucide:clock" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <p class="text-sm text-blue-900">
              A confirmation button will appear 1 hour before the meetup time to confirm the book handoff.
            </p>
          </div>
        </div>

        <!-- Confirmation Button - Show when within 1 hour -->
        <div v-else class="bg-blue-50 border-2 border-blue-300 rounded-lg p-5">
          <div class="mb-4 flex items-start gap-3">
            <Icon name="lucide:alert-circle" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <p class="text-sm text-blue-900 font-medium">
              Please confirm if you have {{ from === 'rental' ? 'received' : 'delivered' }} the book. Both users must confirm to progress the rental.
            </p>
          </div>
          <button 
            v-if="from === 'rental'"
            class="w-full bg-green-500 hover:bg-green-600 text-white px-4 py-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
          >
            <Icon name="lucide:check" class="w-5 h-5" />
            Confirm Received Book
          </button>
          <button 
            v-else-if="from === 'lending'"
            class="w-full bg-green-500 hover:bg-green-600 text-white px-4 py-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
          >
            <Icon name="lucide:check" class="w-5 h-5" />
            Confirm Delivered Book
          </button>
        </div>
      </div>

      <!-- Pending Status Alert - Different for rental vs lending -->
      <div v-if="currentItem.rent_status === 'pending'">
        <!-- For Rental: Waiting for approval -->
        <div v-if="from === 'rental'" 
             class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div class="flex items-start gap-3">
            <Icon name="lucide:info" class="w-5 h-5 text-yellow-600 mt-0.5" />
            <div class="flex-1">
              <p class="text-yellow-800 font-medium">Request Pending: Please wait for the request to be approved by the owner.</p>
            </div>
          </div>
          <button 
            @click="handleCancelRequest"
            class="mt-4 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            Cancel Request
          </button>
        </div>

        <!-- For Lending: Action Required -->
        <div v-else-if="from === 'lending'" 
             class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="flex items-start gap-3">
            <Icon name="lucide:info" class="w-5 h-5 text-blue-600 mt-0.5" />
            <div class="flex-1">
              <p class="text-blue-900 font-medium"><strong>Action Required:</strong> A renter wants to borrow your book. Please approve or reject this request.</p>
            </div>
          </div>
          <div class="flex gap-3 mt-4">
            <button 
              class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
            >
              <Icon name="lucide:check" class="w-4 h-4" />
              Approve Rental
            </button>
            <button 
              class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
            >
              <Icon name="lucide:x" class="w-4 h-4" />
              Reject Rental
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>