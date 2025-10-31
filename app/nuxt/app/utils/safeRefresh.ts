let lastRefresh = 0;

export async function safeRefresh() {
	const now = Date.now();
	if (now - lastRefresh < 10_000) return; // skip if recent
	await useRefreshAccessToken();
	lastRefresh = now;
}