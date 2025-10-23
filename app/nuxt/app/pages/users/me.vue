<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <div class="min-h-screen w-full pt-4 px-4 md:px-8 lg:px-15">
    <div class="mt-20 gap-10 flex flex-col justify-center items-center">
      <ProfileMainSection />
      <ProfileAdditionalInfo />
    </div>
  </div>
</template>
