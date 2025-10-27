
type FetchMethod =
  | 'GET'
  | 'POST'
  | 'PUT'
  | 'DELETE'
  | 'PATCH'
  | 'OPTIONS'
  | 'HEAD';

export default defineNuxtPlugin((nuxtApp) => {
	const baseURL = import.meta.env.VITE_API_URL;

	const apiFetch = $fetch.create({
		baseURL: import.meta.env.VITE_API_URL,
		credentials: 'include',

		async onResponseError({ response, request, options }) {
			if (response.status === 401) {
				try {

					// Attempt to refresh token
					await $fetch(`${baseURL}/api/users/refresh`, {
						method: 'POST',
						credentials: 'include',
					});

					
					// Retry the original request
					return await $fetch(request as string, {
						method: options.method as FetchMethod,
						body: options.body,
						headers: options.headers,
						params: options.params,
						credentials: 'include',
					});

				} catch {
					console.error('Session expired, redirecting to login...');

					if (import.meta.client) {
						await navigateTo('/login');
					}
				}
			}
		},
	});

  nuxtApp.provide('apiFetch', apiFetch);
});