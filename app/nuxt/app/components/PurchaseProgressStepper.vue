<script setup lang="ts">
interface Props {
  status: string;
  from: string;
}

const props = defineProps<Props>();

const getStepperItems = () => {
  if (props.from === 'purchase') {
    return [
      {
        title: 'Requested',
        description: 'Purchase request sent',
        icon: 'i-lucide-send'
      },
      {
        title: 'Confirmed',
        description: 'Seller approved request',
        icon: 'i-lucide-check-circle'
      },
      {
        title: 'Pickup',
        description: 'Ready for pickup',
        icon: 'i-lucide-package'
      },
      {
        title: 'Completed',
        description: 'Purchase finished',
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
        description: 'Purchase request received',
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
        title: 'Completed',
        description: 'Sale finished',
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
    'completed': 3,
    'rate_user': 4
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