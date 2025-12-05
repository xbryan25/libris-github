<script setup lang="ts">
import type { Sale } from '~/composables/useUserSales'
import type { StepperItem } from '@nuxt/ui'

interface Props {
  sale: Sale
}

defineProps<Props>()

const getStatusBadge = (status: string) => {
  const statusConfig: Record<string, { label: string; color: string }> = {
    pending: { label: 'Pending Approval', color: 'bg-yellow-500' },
    approved: { label: 'Confirmed', color: 'bg-blue-500' },
    awaiting_pickup_confirmation: { label: 'Pickup Arranged', color: 'bg-orange-500' },
    completed: { label: 'Sale Complete', color: 'bg-green-500' },
    rate_user: { label: 'Rate Buyer', color: 'bg-amber-500' }
  }
  
  return statusConfig[status] || { label: status, color: 'bg-gray-500' }
}

const getStepperItems = (status: string): StepperItem[] => {
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

const getCurrentStep = (status: string) => {
  const statusMap: Record<string, number> = {
    'pending': 0,
    'approved': 1,
    'awaiting_pickup_confirmation': 2,
    'completed': 3 
  }
  
  return statusMap[status] ?? 0
}
</script>

<template>
  <NuxtLink 
    :to="{
      path: `/purchases/${sale.purchase_id}`,
      query: { from: 'sale' }
    }" 
    class="block"
  >
    <div class="bg-surface rounded-lg border border-base p-6 hover:shadow-md transition-shadow">
      <!-- Header -->
      <div class="flex justify-between items-start mb-4">
        <div class="flex-1">
          <h3 class="text-xl font-bold text-foreground mb-2">{{ sale.title }}</h3>
          <div class="flex items-center gap-4 text-sm text-muted">
            <div class="flex items-center gap-1">
              <Icon name="lucide:user" class="w-4 h-4" />
              <span>Selling to {{ sale.to }}</span>
            </div>
          </div>
        </div>
        
        <!-- Status Badge and Readits -->
        <div class="flex items-center gap-3">
          <span 
            :class="[getStatusBadge(sale.purchase_status).color, 'text-white px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap']"
          >
            {{ getStatusBadge(sale.purchase_status).label }}
          </span>
          <div class="flex items-center gap-1">
            <span class="text-accent text-xl font-bold">+</span>
            <Icon name="fluent:book-coins-20-regular" class="w-6 h-6 text-accent" />
            <span class="text-accent text-xl font-bold">{{ sale.cost }}</span>
          </div>
        </div>
      </div>

      <!-- Progress Steps using UStepper -->
      <div class="mt-6">
        <UStepper 
          disabled
          :items="getStepperItems(sale.purchase_status)" 
          :model-value="getCurrentStep(sale.purchase_status)"
        />
      </div>
    </div>
  </NuxtLink>
</template>