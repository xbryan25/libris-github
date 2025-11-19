<script setup lang="ts">
import { h, resolveComponent } from 'vue';
import type { TableColumn } from '@nuxt/ui';
import { useDebounceFn } from '@vueuse/core';

import type { Notification } from '~/types';

const UCheckbox = resolveComponent('UCheckbox');

const notificationsData = ref<Notification[]>([]);

const selectedRows = ref<Set<string>>(new Set());

const columns: TableColumn<Notification>[] = [
  {
    id: 'select',
    cell: ({ row }) =>
      h(UCheckbox, {
        ui: {
          base: 'cursor-pointer',
        },
        modelValue: computed(() => selectedRows.value.has(row.original.notificationId)).value,
        'onUpdate:modelValue': (value: boolean) => {
          console.log(value);
          toggleRow(row.original.notificationId, value);
        },
        'aria-label': 'Select row',
      }),
    meta: {
      class: {
        th: 'w-12',
        td: 'w-12',
      },
    },
  },
  {
    id: 'notification',
    cell: ({ row }) => {
      return h(
        resolveComponent('NuxtLink'),
        { to: `/notifications/${row.original.notificationId}`, class: 'flex gap-10 no-underline' },
        () => [
          h('p', { class: 'font-bold' }, row.original.header),
          h('p', { class: 'text-sm text-gray-500 truncate' }, row.original.message),
        ],
      );
    },
    meta: {
      class: {
        th: 'max-w-20',
        td: 'max-w-20',
      },
    },
  },
  {
    id: 'date',
    cell: ({ row }) => {
      return h(
        resolveComponent('NuxtLink'),
        { to: `/notifications/${row.original.notificationId}`, class: 'flex gap-10 no-underline' },
        () => [h('p', { class: 'font-bold' }, row.original.createdAt)],
      );
    },
    meta: {
      class: {
        th: 'w-20',
        td: 'w-20',
      },
    },
  },
];

const externalCheckboxValue = computed<boolean | 'indeterminate'>(() => {
  if (selectedRows.value.size === 0) return false;
  if (selectedRows.value.size === notificationsData.value.length) return true;
  return 'indeterminate';
});

// Handler for external checkbox
function toggleAll(value: boolean | 'indeterminate') {
  const val = value === 'indeterminate' ? true : value;
  if (val) selectedRows.value = new Set(notificationsData.value.map((r) => r.notificationId));
  else selectedRows.value = new Set();
}

// Row checkbox toggle
function toggleRow(id: string, value: boolean) {
  const newSet = new Set(selectedRows.value);
  if (value) newSet.add(id);
  else newSet.delete(id);
  selectedRows.value = newSet;
}

const orderItems = ref(['Show Newest First', 'Show Oldest First']);
const order = ref('Show Newest First');

const readStatusItems = ref(['Show All', 'Show Only Read', 'Show Only Unread']);
const readStatus = ref('Show All');

// Table functions

const isLoading = ref(true);

const totalNotificationCount = ref(0);
const pageNumber = ref(1);
const reservedHeight = 300;
const rowsPerPage = ref(0);

const loadEntities = async () => {
  // isLoading.value = true;

  const options = {
    rowsPerPage: rowsPerPage.value,
    pageNumber: pageNumber.value,
    hasReadStatus: readStatus.value,
    order: order.value,
  };

  const data = await useNotifications(options);

  notificationsData.value = data.entities;

  isLoading.value = false;
};

const debouncedLoadEntities = useDebounceFn(async () => {
  isLoading.value = true;

  await loadEntities();
}, 700); // 700ms debounce

const updatePagination = () => {
  calculateRows();
  debouncedGetTotalEntityCount();
};

const calculateRows = () => {
  // const row = document.querySelector('table tbody tr');
  // const rowHeight = row?.clientHeight ? row?.clientHeight - 1 : 63;

  const rowHeight = 64;

  const availableHeight = window.innerHeight - reservedHeight;

  rowsPerPage.value = Math.max(5, Math.floor(availableHeight / rowHeight));
};

const getTotalEntityCount = async () => {
  const { totalCount }: { totalCount: number } = await useNotificationsCount(readStatus.value);

  totalNotificationCount.value = totalCount;
};

const debouncedGetTotalEntityCount = useDebounceFn(async () => {
  await getTotalEntityCount();

  checkIfBeyondPageLimit();
}, 200); // 700ms debounce

const checkIfBeyondPageLimit = () => {
  const totalPages = Math.ceil(totalNotificationCount.value / rowsPerPage.value) || 1;

  // If current page exceeds total pages, clamp it down
  if (pageNumber.value > totalPages) {
    pageNumber.value = totalPages;
  }

  // If there are no records, reset to page 1
  if (totalNotificationCount.value === 0) {
    pageNumber.value = 1;
  }
};

watch(
  [() => rowsPerPage.value, () => pageNumber.value, () => readStatus.value, () => order.value],
  () => {
    isLoading.value = true;
    debouncedLoadEntities();
    debouncedGetTotalEntityCount();
  },
);

onMounted(() => {
  updatePagination();

  debouncedLoadEntities();

  window.addEventListener('resize', updatePagination);
});
</script>

<template>
  <div class="flex-1 flex flex-col items-center px-20">
    <div class="flex w-full">
      <div class="flex-1 flex gap-3 items-center pl-[15px]">
        <UCheckbox
          :model-value="externalCheckboxValue"
          :ui="{ base: 'cursor-pointer' }"
          @update:model-value="toggleAll"
        />

        <UTooltip v-if="externalCheckboxValue" text="Delete">
          <UButton icon="material-symbols:delete-outline" color="neutral" class="cursor-pointer" />
        </UTooltip>

        <UTooltip v-if="externalCheckboxValue" text="Mark as read">
          <UButton icon="material-symbols:mark-email-read" color="neutral" class="cursor-pointer" />
        </UTooltip>
      </div>

      <div class="flex-1 flex justify-end gap-3">
        <USelect v-model="readStatus" :items="readStatusItems" class="min-w-45" />
        <USelect v-model="order" :items="orderItems" class="min-w-45" />
      </div>
    </div>

    <UTable
      ref="table"
      :data="notificationsData"
      :columns="columns"
      class="flex-1"
      :ui="{ root: 'table-auto !w-full !min-w-0' }"
      :meta="{
        class: {
          tr: (row) =>
            row.original.isRead
              ? 'cursor-pointer hover:outline hover:outline-1 hover:outline-surface'
              : 'cursor-pointer hover:outline hover:outline-1 hover:outline-surface bg-surface ',
        },
      }"
    />

    <UPagination show-edges :sibling-count="2" :total="10" class="pt-5" />
  </div>
</template>
