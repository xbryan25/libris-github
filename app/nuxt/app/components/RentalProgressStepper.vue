<script setup lang="ts">
interface Props {
  status: string;
  from: string;
}

const props = defineProps<Props>();

const getStepperItems = () => {
  if (props.from === 'rental') {
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
      },  
      {
        title: 'Rate',
        description: 'Rate the experience',
        icon: 'i-lucide-star'
      },
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
        description: 'Currently lending',
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
      },
      {
        title: 'Rate',
        description: 'Rate the experience',
        icon: 'i-lucide-star'
      }
    ]
  }
}

const getCurrentStep = () => {
  const statusMap: Record<string, number> = {
    'pending': 0,
    'approved': 1,
    'awaiting_pickup_confirmation': 2,
    'ongoing': 3,
    'awaiting_return_confirmation': 4,
    'completed': 5,
    'rate_user': 6
  }
  
  return statusMap[props.status] ?? 0
}
</script>

<template>
  <div class="bg-surface rounded-lg border border-base p-6">
    <UStepper 
      disabled
      :items="getStepperItems()" 
      :model-value="getCurrentStep()"
    />
  </div>
</template>