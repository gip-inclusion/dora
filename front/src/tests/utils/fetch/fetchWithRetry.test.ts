import { beforeEach, describe, expect, test, vi } from "vitest";
import { fetchWithRetry } from "$lib/utils/fetch-retry";
import { sleep } from "$lib/utils/misc";

vi.mock("$lib/utils/misc", () => ({
  // on mocke la fonction sleep pour ne pas attendre réellement durant les tests
  sleep: vi.fn().mockResolvedValue(undefined),
}));

describe("fetchWithRetry", () => {
  const sleepMock = vi.mocked(sleep);

  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("retourne la reponse immediatement si le status n'est pas 5xx", async () => {
    const fetchFn = vi
      .fn()
      .mockResolvedValue(new Response(null, { status: 200 }));

    const response = await fetchWithRetry("https://example.com", undefined, {
      fetchFn,
    });

    expect(response.status).toBe(200);
    expect(fetchFn).toHaveBeenCalledTimes(1);
    expect(sleepMock).not.toHaveBeenCalled();
  });

  test("retente quand le serveur renvoie 5xx puis réussit", async () => {
    const fetchFn = vi
      .fn()
      .mockResolvedValueOnce(new Response(null, { status: 500 }))
      .mockResolvedValueOnce(new Response(null, { status: 200 }));

    const response = await fetchWithRetry("https://example.com", undefined, {
      fetchFn,
      maxAttempts: 3,
    });

    expect(response.status).toBe(200);
    expect(fetchFn).toHaveBeenCalledTimes(2);
    expect(sleepMock).toHaveBeenCalledTimes(1);
  });

  test("renvoie la dernière réponse 5xx quand maxAttempts est atteint", async () => {
    const fetchFn = vi
      .fn()
      .mockResolvedValue(new Response(null, { status: 503 }));

    const response = await fetchWithRetry("https://example.com", undefined, {
      fetchFn,
      maxAttempts: 3,
    });

    expect(response.status).toBe(503);
    expect(fetchFn).toHaveBeenCalledTimes(3);
    expect(sleepMock).toHaveBeenCalledTimes(2);
  });

  test("retente apres une erreur reseau puis réussit", async () => {
    const fetchFn = vi
      .fn()
      .mockRejectedValueOnce(new TypeError("network error"))
      .mockResolvedValueOnce(new Response(null, { status: 200 }));

    const response = await fetchWithRetry("https://example.com", undefined, {
      fetchFn,
      maxAttempts: 2,
    });

    expect(response.status).toBe(200);
    expect(fetchFn).toHaveBeenCalledTimes(2);
    expect(sleepMock).toHaveBeenCalledTimes(1);
  });

  test("propage l'erreur réseau quand maxAttempts est atteint", async () => {
    const fetchFn = vi.fn().mockRejectedValue(new TypeError("network error"));

    await expect(
      fetchWithRetry("https://example.com", undefined, {
        fetchFn,
        maxAttempts: 2,
      })
    ).rejects.toThrow("network error");

    expect(fetchFn).toHaveBeenCalledTimes(2);
    expect(sleepMock).toHaveBeenCalledTimes(1);
  });
});
