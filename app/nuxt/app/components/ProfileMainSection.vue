<script setup lang="ts">
import TrustScoreDetails from './TrustScoreDetails.vue';
import ProfilePictureUpload from './ProfilePictureUpload.vue';
import type { Profile } from '~/composables/UseProfile';
import { computed, onMounted, watch } from 'vue';
import { useTrustScorePercentile } from '~/composables/useTrustScorePercentile';
import { useProfileEdit } from '~/composables/useProfileEdit';

interface Props {
  profile: Profile | null;
  loading: boolean;
  error: string | null;
  userId?: string;
  isCurrentUser?: boolean;
  isEditing?: boolean;
  editForm?: any;
}

const props = defineProps<Props>();

const { percentile, fetchPercentile, getPercentileText } = useTrustScorePercentile(props.userId);

const {
  saving,
  error: editError,
  success,
  startEditing,
  cancelEditing,
  saveProfile,
} = useProfileEdit();

const editForm = computed(() => props.editForm || {});
const isEditing = computed(() => props.isEditing || false);

const emit = defineEmits<{
  profileUpdated: [profile: any];
  imageUpdated: [imageUrl: string];
}>();

const trustScoreBadge = computed(() => {
  if (props.profile?.trust_score === null || props.profile?.trust_score === undefined)
    return { text: 'Unknown', color: 'bg-gray-500' };

  const score = props.profile.trust_score;

  if (score >= 951) return { text: 'Perfect', color: 'bg-[#15803D]' };
  if (score >= 751) return { text: 'Exceptional', color: 'bg-[#22C55E]' };
  if (score >= 500) return { text: 'Good', color: 'bg-[#84CC16]' };
  if (score >= 251) return { text: 'Decent', color: 'bg-[#FACC15]' };
  if (score >= 51) return { text: 'Bad', color: 'bg-[#CA8A04]' };
  return { text: 'Poor', color: 'bg-[#000000]' };
});

watch(
  () => props.profile,
  (newProfile) => {
    if (newProfile?.trust_score) {
      fetchPercentile();
    }
  },
  { immediate: true },
);

const handleEdit = () => {
  startEditing(props.profile);
};

const handleSave = async () => {
  const updatedProfile = await saveProfile();
  if (updatedProfile) {
    emit('profileUpdated', updatedProfile);
  }
};

const handleCancel = () => {
  cancelEditing();
};

const handleImageUpdate = (imageUrl: string) => {
  emit('imageUpdated', imageUrl);
};

const formattedFullName = computed(() => {
  const first = props.profile?.first_name?.trim() || '';
  const middle = props.profile?.middle_name?.trim() || '';
  const last = props.profile?.last_name?.trim() || '';

  if (!first && !middle && !last) return '-';

  if (first && last && middle) return `${first} ${middle.charAt(0)}. ${last}`;
  if (first && last) return `${first} ${last}`;
  if (first && middle) return `${first} ${middle.charAt(0)}.`;
  if (middle && last) return `${middle.charAt(0)}. ${last}`;
  if (first) return first;
  if (last) return last;
  return '-';
});

onMounted(() => {
  if (props.profile?.trust_score) {
    fetchPercentile();
  }
});
</script>

<template>
  <UCard
    v-if="loading"
    class="w-full max-w-[1500px] h-auto bg-surface border-base flex flex-col md:flex-row items-stretch px-6 py-6"
  >
    <div class="flex items-center justify-start space-x-6 flex-grow">
      <USkeleton class="w-35 h-35 rounded-full" />

      <div class="flex flex-col justify-center space-y-3">
        <USkeleton class="h-12 w-64" />
        <USkeleton class="h-10 w-80" />
        <USkeleton class="h-8 w-48" />
      </div>

      <div class="flex items-center h-full">
        <USeparator orientation="vertical" class="h-[200px] border-base ml-130" type="solid" />
      </div>

      <div class="flex flex-col space-y-3">
        <div class="flex items-center space-x-2">
          <USkeleton class="h-10 w-32" />
          <USkeleton class="w-6 h-6 rounded-full" />
        </div>
        <div class="flex items-center space-x-3">
          <USkeleton class="h-12 w-20" />
          <USkeleton class="h-8 w-16 rounded-full" />
        </div>
        <USkeleton class="h-4 w-48" />
      </div>
    </div>
  </UCard>

  <div
    v-else-if="error"
    class="w-full max-w-[1500px] bg-surface border-base flex items-center justify-center p-6"
  >
    <div class="text-lg text-red-500">Error: {{ error }}</div>
  </div>

  <div
    v-else
    class="w-full max-w-[1500px] h-auto bg-white dark:bg-zinc-950 border border-zinc-300 dark:border-zinc-800 border-radius rounded-lg flex flex-col md:flex-row items-stretch px-6 py-6"
  >
    <div class="flex items-center justify-start space-x-6 flex-grow">
      <ProfilePictureUpload
        v-if="isCurrentUser"
        :current-image-url="profile?.profile_image_url"
        :user-id="profile?.username || ''"
        @image-updated="handleImageUpdate"
      />
      <div v-else-if="profile?.profile_image_url" class="w-35 h-35 rounded-full overflow-hidden">
        <img
          :src="profile.profile_image_url"
          :alt="`${profile.first_name} ${profile.last_name}'s profile picture`"
          class="w-full h-full object-cover"
        />
      </div>
      <Icon v-else name="heroicons:user-circle" class="w-35 h-35 rounded-full" />

      <div class="flex-1 flex flex-col justify-center">
        <div class="text-[42px] font-bold text-base truncate" :title="profile?.username">
          {{ profile?.username || '-' }}
        </div>

        <div class="text-[35px] font-bold text-base truncate w-full" :title="formattedFullName">
          {{ formattedFullName }}
        </div>

        <div class="text-[25px] font-bold text-muted">
          Joined since {{ profile?.account_activated_at || '-' }}
        </div>
      </div>

      <div class="flex items-center h-full">
        <USeparator orientation="vertical" class="h-[200px] border-base" type="solid" />
      </div>

      <div class="flex flex-col">
        <div class="flex items-center space-x-2">
          <div class="text-[35px] font-extrabold text-base whitespace-nowrap">Trust Score</div>
          <TrustScoreDetails />
        </div>

        <div class="flex items-center space-x-3">
          <div class="text-[40px] font-semibold text-base">{{ profile?.trust_score }}</div>
          <UBadge
            :class="[
              trustScoreBadge.color,
              'text-white text-center px-3 py-1',
              trustScoreBadge.text === 'Poor' ? 'border border-white' : '',
            ]"
            variant="solid"
          >
            {{ trustScoreBadge.text }}
          </UBadge>
        </div>

        <div class="text-[15px] font-semibold text-muted">{{ getPercentileText() }}</div>
      </div>
    </div>
  </div>
</template>
