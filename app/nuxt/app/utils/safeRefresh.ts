let lastRefresh = 0;

export async function safeRefresh(runType: 'client' | 'server', cookie?: string) {
  const now = Date.now();
  if (now - lastRefresh < 10_000) return; // skip if recent
  await useRefreshAccessToken(runType, cookie);
  lastRefresh = now;
}