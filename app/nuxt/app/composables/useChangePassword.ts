export const useRequestChangePasswordCode = async () => {
  const { $apiFetch } = useNuxtApp();

  const response = await $apiFetch(`/api/users/change-password/request-code`, {
    method: "POST",
    credentials: "include",
  });

  console.log("[COMPOSABLE] Request change password code response:", response);
  return response;
};

export const useVerifyChangePasswordCode = async (code: string) => {
  const { $apiFetch } = useNuxtApp();

  const response = await $apiFetch(`/api/users/change-password/verify-code`, {
    method: "POST",
    credentials: "include",
    body: {
      code,
    },
  });

  console.log("[COMPOSABLE] Verify change password code response:", response);
  return response;
};

export const useChangePassword = async (
  code: string,
  currentPassword: string,
  newPassword: string
) => {
  const { $apiFetch } = useNuxtApp();

  const response = await $apiFetch(`/api/users/change-password`, {
    method: "POST",
    credentials: "include",
    body: {
      code,
      currentPassword,
      newPassword,
    },
  });

  console.log("[COMPOSABLE] Change password response:", response);
  return response;
};

export const useResendChangePasswordCode = async () => {
  const { $apiFetch } = useNuxtApp();

  const response = await $apiFetch(`/api/users/change-password/resend-code`, {
    method: "POST",
    credentials: "include",
  });

  console.log("[COMPOSABLE] Resend change password code response:", response);
  return response;
};