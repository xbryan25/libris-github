<script setup lang="ts">
interface Props {
  cost: number;
  allFeesCaptured: boolean;
  from: string;
  securityDeposit: number;
  dailyRate: number;
  rentalDurationDays: number;
}

const props = defineProps<Props>();
</script>

<template>
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
          <span class="font-bold text-lg text-accent">{{ securityDeposit }}</span>
        </div>
      </div>
      
      <div>
        <p class="text-xs text-muted mb-1">Daily Rate</p>
        <div class="flex items-center gap-1">
          <Icon name="fluent:book-coins-20-regular" class="w-4 h-4 text-accent" />
          <span class="font-bold text-lg text-accent">{{ dailyRate }}</span>
        </div>
      </div>

      <div>
        <p class="text-xs text-muted mb-1">Rental Cost ({{ rentalDurationDays }}d)</p>
        <div class="flex items-center gap-1">
          <Icon name="fluent:book-coins-20-regular" class="w-4 h-4 text-accent" />
          <span class="font-bold text-lg text-accent">{{ dailyRate * rentalDurationDays }}</span>
        </div>
      </div>

      <div>
        <p class="text-xs text-muted mb-1">Total Cost</p>
        <div class="flex items-center gap-1">
          <span class="text-sm font-bold text-accent">{{ from === 'rental' ? '-' : '+' }}</span>
          <Icon name="fluent:book-coins-20-regular" class="w-4 h-4 text-accent" />
          <span class="font-bold text-lg text-accent">{{ cost }}</span>
        </div>
      </div>
    </div>

    <div class="mt-4 pt-4 border-t border-base">
      <div class="flex items-center justify-between">
        <p class="text-sm text-muted">Payment Status</p>
        <p class="font-medium text-sm" :class="allFeesCaptured ? 'text-green-600' : 'text-yellow-600'">
          {{ allFeesCaptured ? '✓ Captured' : '⏳ Pending' }}
        </p>
      </div>
    </div>
  </div>
</template>