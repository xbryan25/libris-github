

type FetchMethod =
  | 'GET'
  | 'POST'
  | 'PUT'
  | 'DELETE'
  | 'PATCH'
  | 'OPTIONS'
  | 'HEAD';

let refreshPromise: Promise<string | null> | null = null;

export default defineNuxtPlugin((nuxtApp) => {
  const baseURL = import.meta.env.VITE_API_URL;

  const apiFetch = $fetch.create({
    baseURL,
    credentials: 'include',

    async onResponseError({ response, request, options }) {
      if (response.status !== 401) {
        throw response._data ?? response;
      }

      try {
        // Prevent multiple simultaneous refresh calls
        if (!refreshPromise) {
          refreshPromise = (async () => {
            // SPA: browser handles HttpOnly cookies automatically
            await $fetch(`${baseURL}/api/users/refresh`, {
              method: 'POST',
              credentials: 'include',
            });
            return null;
          })().finally(() => (refreshPromise = null));
        }

        await refreshPromise;

        // Retry the original request
        const requestUrl = typeof request === 'string' ? request : request.url;
        const retryUrl = requestUrl.startsWith('http') ? requestUrl : `${baseURL}${requestUrl}`;

        await $fetch.raw(retryUrl, {
          method: options.method as FetchMethod,
          body: options.body,
          headers: {
            ...options.headers,
          },
          params: options.params,
          credentials: 'include',
        });

      } catch (err) {
        console.error('[apiFetch] Session expired, redirecting to login...', err);
        if (import.meta.client) {
          await navigateTo('/login');
        }
        throw new Error('SessionExpired');
      }
    },
  });

  nuxtApp.provide('apiFetch', apiFetch);
});