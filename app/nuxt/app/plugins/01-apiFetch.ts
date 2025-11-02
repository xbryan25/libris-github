

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
            if (import.meta.server) {
              // SSR: forward current cookies
              const event = nuxtApp.ssrContext?.event;
              const oldCookie = event?.node?.req?.headers.cookie;

              const refreshResponse = await $fetch.raw(`${baseURL}/api/users/refresh`, {
                method: 'POST',
                headers: oldCookie ? { cookie: oldCookie } : undefined,
                credentials: 'omit',
              });

              let newCookie: string | null = null;
              if (refreshResponse.headers) {
                const setCookies = refreshResponse.headers.getSetCookie?.();
                if (setCookies?.length) {
                  // Forward Set-Cookie to client
                  event?.node?.res.setHeader('set-cookie', setCookies);
                  // Update in-memory cookie for retry
                  newCookie = setCookies.map(c => c.split(';')[0]).join('; ');
                }
              }

              return newCookie;
            } else {
              // SPA: browser handles HttpOnly cookies automatically
              await $fetch(`${baseURL}/api/users/refresh`, {
                method: 'POST',
                credentials: 'include',
              });
              return null;
            }
          })().finally(() => (refreshPromise = null));
        }

        const newCookieHeader = await refreshPromise;

        // Retry the original request
        const requestUrl = typeof request === 'string' ? request : request.url;
        const retryUrl = requestUrl.startsWith('http') ? requestUrl : `${baseURL}${requestUrl}`;

        await $fetch.raw(retryUrl, {
			method: options.method as FetchMethod,
			body: options.body,
			headers: {
				...options.headers,
				...(import.meta.server && newCookieHeader ? { cookie: newCookieHeader } : {}),
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