<script setup lang="ts">
  interface Props {
    activeTab: 'lending' | 'renting';
  }

  defineProps<Props>();
</script>

<template>
  <div class="w-full bg-background">
    <div v-if="activeTab === 'lending'">
      <!-- Lending content goes here -->
      <div class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center"> 
          <div class="text-center">
            <UIcon name="bytesize:book" class="w-16 h-16 text-muted mx-auto" />
            <p class="text-muted mt-4 text-lg">Lending content will be displayed here</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <!-- Renting content goes here -->
      <div class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="bytesize:book" class="w-16 h-16 text-muted mx-auto" />
            <p class="text-muted mt-4 text-lg">Renting content will be displayed here</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>