import { sleep } from "$lib/utils/misc";

export type FetchRetryOptions = {
  maxAttempts?: number;
  fetchFn?: typeof fetch;
};

/**
 * `fetch` avec retry (ex: 500/504) + backoff + timeout.
 * Ne monkey-patche pas `window.fetch`: l'appelant choisit explicitement de l'utiliser.
 */
export function fetchWithRetry(
  input: RequestInfo | URL,
  init?: RequestInit,
  options?: FetchRetryOptions
): Promise<Response> {
  const fetchFn = options?.fetchFn ?? fetch;
  const maxAttempts = options?.maxAttempts ?? 3;

  async function attempt(attemptIndex: number): Promise<Response> {
    try {
      const response = await fetchFn(input, init);
      if (response.status < 500 || response.status >= 600) {
        return response;
      }
      if (attemptIndex === maxAttempts - 1) {
        return response;
      }
    } catch (error) {
      if (attemptIndex === maxAttempts - 1 || init?.signal?.aborted) {
        throw error;
      }
    }

    const exponentialBackoff = 250 * Math.pow(2, attemptIndex);
    const boundedBackoff = Math.min(1000, exponentialBackoff);
    const jitter = Math.random() * 150;
    const delayMs = boundedBackoff + jitter;
    await sleep(delayMs);
    return attempt(attemptIndex + 1);
  }

  return attempt(0);
}
