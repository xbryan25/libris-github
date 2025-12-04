<script setup lang="ts">
interface Props {
  status: string;
  from: string;
  transferDecisionPending?: boolean; // Updated prop name
}

const props = defineProps<Props>();

// Debug log
console.log('Stepper props:', {
  status: props.status,
  from: props.from,
  transferDecisionPending: props.transferDecisionPending
});

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
        title: 'Transfer',
        description: 'Ownership transfer',
        icon: 'i-lucide-refresh-cw'
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
    // For sales (seller view), no Transfer step
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
  console.log('getCurrentStep called:', {
    from: props.from,
    status: props.status,
    transferDecisionPending: props.transferDecisionPending
  });
  
  // For purchases (buyer view), include Transfer step
  if (props.from === 'purchase') {
    // If status is completed but transfer is pending, show step 3 (Transfer)
    if (props.status === 'completed' && props.transferDecisionPending === true) {
      console.log('Returning step 3 (Transfer)');
      return 3;
    }
    
    const statusMap: Record<string, number> = {
      'pending': 0,
      'approved': 1,
      'awaiting_pickup_confirmation': 2,
      'completed': 4, // After transfer decision is made
      'rate_user': 5
    }
    const step = statusMap[props.status] ?? 0;
    console.log('Returning step from statusMap:', step);
    return step;
  } else {
    // For sales (seller view), no Transfer step
    const statusMap: Record<string, number> = {
      'pending': 0,
      'approved': 1,
      'awaiting_pickup_confirmation': 2,
      'completed': 3,
      'rate_user': 4
    }
    return statusMap[props.status] ?? 0
  }
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