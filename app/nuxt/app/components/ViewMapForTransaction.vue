<script setup lang="ts">
const latitude = ref(null);
const longitude = ref(null);
const address = ref('');

const props = defineProps<{ isOpenViewMapForTransaction: boolean }>();

const emit = defineEmits<{
  (e: 'update:openViewMapForTransaction', value: boolean): void;
  (e: 'update:selectedAddress', address: string): void;
  (e: 'update:latitudeAndLongitude', latitude: number, longitude: number): void;
}>();

const onMapClick = async (e) => {
  latitude.value = e.latlng.lat;
  longitude.value = e.latlng.lng;

  // Reverse geocode
  const res = await $fetch(
    `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude.value}&lon=${longitude.value}`,
  );

  address.value = res.display_name;

  emit('update:selectedAddress', address.value);
  emit('update:openViewMapForTransaction', false);
};

const isOpenMapForTransaction = computed({
  get: () => props.isOpenViewMapForTransaction,
  set: (val: boolean) => {
    emit('update:openViewMapForTransaction', val);
  },
});
</script>

<template>
  <UModal v-model:open="isOpenMapForTransaction" :ui="{ content: 'max-w-[90vw]' }">
    <template #content>
      <div class="flex">
        <LMap
          ref="map"
          :zoom="12"
          :center="[14.599512, 120.984222]"
          :use-global-leaflet="false"
          style="height: 90vh"
          @click="onMapClick"
        >
          <LTileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&amp;copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            layer-type="base"
            name="OpenStreetMap"
          />

          <LMarker
            v-if="latitude !== null && longitude !== null"
            :lat-lng="[latitude, longitude]"
          />
        </LMap>
      </div>
    </template>
  </UModal>
</template>
