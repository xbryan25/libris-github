<script setup lang="ts">
import L from 'leaflet';
import 'leaflet-control-geocoder';
import 'leaflet/dist/leaflet.css';
import 'leaflet-control-geocoder/dist/Control.Geocoder.css';

const latitude = ref<number | null>(null);
const longitude = ref<number | null>(null);
const address = ref('');

const props = defineProps<{ isOpenViewMapForTransaction: boolean; removeMapMarker: number }>();

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
  emit('update:latitudeAndLongitude', latitude.value as number, longitude.value as number);
  emit('update:openViewMapForTransaction', false);
};

const isOpenMapForTransaction = computed({
  get: () => props.isOpenViewMapForTransaction,
  set: (val: boolean) => {
    emit('update:openViewMapForTransaction', val);
  },
});

function onMapReady(map: L.Map) {
  // @ts-expect-error testtestsss
  const geocoder = L.Control.geocoder({
    placeholder: 'Search location...',
    defaultMarkGeocode: false, // we’ll handle marker ourselves
  }).addTo(map);

  geocoder.on('markgeocode', async (e: any) => {
    const center = e.geocode.center;
    latitude.value = center.lat;
    longitude.value = center.lng;

    const res = await $fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude.value}&lon=${longitude.value}`,
    );

    address.value = res.display_name;

    // Optionally, move map to result
    map.setView(center, map.getZoom());

    emit('update:selectedAddress', address.value);
    emit('update:latitudeAndLongitude', latitude.value as number, longitude.value as number);
    emit('update:openViewMapForTransaction', false);
  });
}

watch(
  () => props.removeMapMarker,
  () => {
    latitude.value = null;
    longitude.value = null;
  },
);
</script>

<template>
  <UModal v-model:open="isOpenMapForTransaction" :ui="{ content: 'max-w-[90vw]' }">
    <template #content>
      <div class="flex">
        <LMap
          ref="map"
          :zoom="12"
          :center="[latitude ? latitude : 14.599512, longitude ? longitude : 120.984222]"
          :use-global-leaflet="false"
          style="height: 90vh"
          @click="onMapClick"
          @ready="onMapReady"
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

          <LControlScale position="bottomright" :imperial="false" :metric="true" />
        </LMap>
      </div>
    </template>
  </UModal>
</template>

<style>
/* Force geocoder input styles */
.leaflet-control.leaflet-control-geocoder input {
  font-family: Inter, ui-sans-serif, system-ui !important;
  color: #111 !important;
  background-color: #fff !important;
  opacity: 1 !important;
  font-weight: 400;
}

/* Placeholder text */
.leaflet-control.leaflet-control-geocoder input::placeholder {
  font-family: Inter, ui-sans-serif, system-ui !important;
  color: #6b7280 !important; /* Tailwind gray-500 */
  opacity: 1 !important;
}

/* Dropdown container */
.leaflet-control-geocoder-alternatives {
  font-family: Inter, ui-sans-serif, system-ui !important;
  background-color: #fff !important;
  color: #111 !important;
}

/* Dropdown items */
.leaflet-control-geocoder-alternatives li {
  font-family: Inter, ui-sans-serif, system-ui !important;
  font-family: inherit !important;
  color: #111 !important;
}

/* Hover state */
.leaflet-control-geocoder-alternatives li:hover {
  font-family: Inter, ui-sans-serif, system-ui !important;
  background-color: #f3f4f6 !important; /* gray-100 */
}
</style>
