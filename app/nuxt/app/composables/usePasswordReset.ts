export const useRequestPasswordReset = async (emailAddress: string) => {
  const { $apiFetch } = useNuxtApp();

  const response = await $apiFetch(`/api/users/forgot-password`, {
    method: "POST",
    credentials: "include",
    body: {
      emailAddress,
    },
  });

  console.log("[COMPOSABLE] Request password reset response:", response);
  return response;
};

export const useVerifyResetCode = async (userId: string, code: string) => {
  const { $apiFetch } = useNuxtApp();

  const response = await $apiFetch(`/api/users/verify-reset-code`, {
    method: "POST",
    credentials: "include",
    body: {
      userId,
      code,
    },
  });

  console.log("[COMPOSABLE] Verify reset code response:", response);
  return response;
};

export const useResetPassword = async (
  userId: string,
  code: string,
  newPassword: string
) => {
  const { $apiFetch } = useNuxtApp();

  const response = await $apiFetch(`/api/users/reset-password`, {
    method: "POST",
    credentials: "include",
    body: {
      userId,
      code,
      newPassword,
    },
  });

  console.log("[COMPOSABLE] Reset password response:", response);
  return response;
};

export const useResendResetCode = async (userId: string) => {
  const { $apiFetch } = useNuxtApp();

  const response = await $apiFetch(`/api/users/resend-reset-code`, {
    method: "POST",
    credentials: "include",
    body: {
      userId,
    },
  });

  console.log("[COMPOSABLE] Resend reset code response:", response);
  return response;
};