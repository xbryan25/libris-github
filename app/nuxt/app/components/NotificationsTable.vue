<script setup lang="ts">
import { h, resolveComponent } from 'vue';
import type { TableColumn } from '@nuxt/ui';
import { useDebounceFn } from '@vueuse/core';

import type { Notification } from '~/types';

import { dateConverter } from '#imports';

import { useAuthStore } from '~/stores/useAuthStore';

const UCheckbox = resolveComponent('UCheckbox');

const notificationsData = ref<Notification[]>([]);

const selectedRows = ref<Set<string>>(new Set());

const clickedRow = ref<Notification | null>(null);

const clickedFromTable = ref<boolean>(false);

const columns: TableColumn<Notification>[] = [
  {
    id: 'select',
    cell: ({ row }) =>
      h(UCheckbox, {
        ui: {
          base: 'cursor-pointer',
        },
        disabled: isLoading.value,
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
        'div',
        {
          class: 'flex gap-10 no-underline',
          onClick: async () => {
            isOpenNotificationModal.value = true;
            row.original.isRead = true;
            clickedRow.value = row.original;
            clickedFromTable.value = true;

            await markSingleNotificationAsRead(row.original.notificationId);
          },
        },
        [
          h('p', { class: 'font-bold min-w-40' }, row.original.header),
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
        'div',
        {
          class: 'flex gap-10 no-underline',
          onClick: async () => {
            isOpenNotificationModal.value = true;
            row.original.isRead = true;
            clickedRow.value = row.original;

            await useMarkNotificationAsRead(row.original.notificationId);
          },
        },
        [h('p', { class: 'font-bold' }, dateConverter(row.original.createdAt, 'short'))],
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

const table = useTemplateRef('table');

const isOpenNotificationModal = ref(false);
const isOpenNotificationActionsModal = ref(false);
const selectedNotificationAction = ref('');

const orderItems = ref(['Show Newest First', 'Show Oldest First']);
const order = ref('Show Newest First');

const readStatusItems = ref(['Show All', 'Show Only Read', 'Show Only Unread']);
const readStatus = ref('Show All');

const rowsPerPageItems = ref([10, 25, 50]);
const rowsPerPage = ref(10);
const delayedRowsPerPage = ref(10);

// Table functions

const isLoading = ref(true);

const totalNotificationCount = ref(0);

const pageNumber = ref(1);
const delayedPageNumber = ref(1);

const authStore = useAuthStore();

const { updateUnreadNotificationsCount } = useSocket(authStore.userId as string);

const loadEntities = async () => {
  isLoading.value = true;

  const options = {
    rowsPerPage: rowsPerPage.value,
    pageNumber: pageNumber.value,
    readStatus: readStatus.value,
    order: order.value,
  };

  const data = await useNotifications(options);

  notificationsData.value = data;

  isLoading.value = false;
};

const debouncedLoadEntities = useDebounceFn(async () => {
  isLoading.value = true;

  await loadEntities();
}, 700); // 700ms debounce

const updatePagination = () => {
  debouncedGetTotalEntityCount();
};

const getTotalEntityCount = async () => {
  const { totalCount }: { totalCount: number } = await useNotificationsTotalCount(readStatus.value);

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

const determineIsReadChange = computed(() => {
  const notificationMap = new Map(notificationsData.value.map((n) => [n.notificationId, n]));

  for (const notificationId of selectedRows.value) {
    const notification = notificationMap.get(notificationId);
    if (!notification) return false;

    if (!notification.isRead) {
      return true;
    }
  }

  return false;
});

const markSingleNotificationAsRead = async (notificationId: string) => {
  await useMarkNotificationAsRead(notificationId);
};

watch(
  [() => rowsPerPage.value, () => pageNumber.value, () => readStatus.value, () => order.value],
  async () => {
    isLoading.value = true;

    await debouncedLoadEntities();

    // Reset selected rows
    selectedRows.value = new Set();
    await debouncedGetTotalEntityCount();

    isLoading.value = false;
  },
);

watch(isLoading, (newVal) => {
  if (!newVal) {
    delayedPageNumber.value = pageNumber.value;
    delayedRowsPerPage.value = rowsPerPage.value;
  }
});

watch(
  () => updateUnreadNotificationsCount.value,
  async () => {
    if (!clickedFromTable.value) {
      await debouncedLoadEntities();
    }

    clickedFromTable.value = false;
  },
);

onMounted(() => {
  updatePagination();

  debouncedLoadEntities();

  window.addEventListener('resize', updatePagination);
});
</script>

<template>
  <div class="flex-1 flex flex-col items-center px-20 py-5">
    <div class="flex w-full">
      <div class="flex-1 flex gap-3 items-center pl-[15px]">
        <div v-if="notificationsData.length > 0 && !isLoading" class="flex gap-3">
          <UCheckbox
            :model-value="externalCheckboxValue"
            :ui="{ base: 'cursor-pointer' }"
            @update:model-value="toggleAll"
          />

          <div class="text-sm text-muted">
            {{ selectedRows.size }} of
            {{ table?.tableApi?.getFilteredRowModel().rows.length || 0 }} row(s) selected
          </div>
        </div>

        <div v-if="externalCheckboxValue && !isLoading" class="flex gap-3">
          <UTooltip text="Delete">
            <UButton
              icon="material-symbols:delete-outline"
              color="neutral"
              class="cursor-pointer"
              @click="
                () => {
                  selectedNotificationAction = 'delete';
                  isOpenNotificationActionsModal = true;
                }
              "
            />
          </UTooltip>

          <UTooltip :text="`Mark as ${determineIsReadChange ? 'read' : 'unread'}`">
            <UButton
              :icon="
                determineIsReadChange
                  ? 'material-symbols:mark-email-read'
                  : 'material-symbols:mark-email-unread'
              "
              color="neutral"
              class="cursor-pointer"
              @click="
                () => {
                  selectedNotificationAction = `${determineIsReadChange ? 'markRead' : 'markUnread'}`;
                  isOpenNotificationActionsModal = true;
                }
              "
            />
          </UTooltip>
        </div>
      </div>

      <div class="flex-1 flex justify-end gap-3">
        <USelect v-model="readStatus" :items="readStatusItems" class="min-w-45" />
        <USelect v-model="order" :items="orderItems" class="min-w-45" />
        <USelect v-model="rowsPerPage" :items="rowsPerPageItems" class="w-18" />
      </div>
    </div>

    <UTable
      ref="table"
      :loading="isLoading"
      :data="notificationsData"
      :columns="columns"
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

    <div v-if="notificationsData.length > 0" class="grid grid-cols-3 pt-5 w-full items-center">
      <div v-if="notificationsData.length == 1" class="text-sm text-muted">
        1 of {{ totalNotificationCount }}.
      </div>
      <div v-else class="text-sm text-muted">
        {{ delayedRowsPerPage * (delayedPageNumber - 1) + 1 }}-{{
          delayedRowsPerPage * delayedPageNumber > totalNotificationCount
            ? totalNotificationCount
            : delayedRowsPerPage * delayedPageNumber
        }}
        of {{ totalNotificationCount }}.
      </div>
      <UPagination
        v-model:page="pageNumber"
        show-edges
        :sibling-count="2"
        :items-per-page="rowsPerPage"
        :total="totalNotificationCount"
        class="flex justify-center"
      />
    </div>

    <NotificationDetailsModal
      :is-open-notification-modal="isOpenNotificationModal"
      :header="clickedRow?.header"
      :message="clickedRow?.message"
      :created-at="clickedRow?.createdAt"
      @update:open-notification-modal="
        (newIsOpenNotificationModal: boolean) =>
          (isOpenNotificationModal = newIsOpenNotificationModal)
      "
    />

    <NotificationActionsModal
      :is-open-notification-actions-modal="isOpenNotificationActionsModal"
      :selected-notification-action="selectedNotificationAction"
      :selected-rows="selectedRows"
      :determine-is-read-change="determineIsReadChange"
      @update:open-notification-actions-modal="
        (newIsOpenNotificationActionsModal: boolean) =>
          (isOpenNotificationActionsModal = newIsOpenNotificationActionsModal)
      "
      @on-successful-action="async () => await debouncedLoadEntities()"
    />
  </div>
</template>
