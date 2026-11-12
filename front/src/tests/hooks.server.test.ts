import { beforeEach, describe, expect, test, vi } from "vitest";

import { UNEXPECTED_ERROR_MESSAGE } from "#lib/consts.ts";

vi.mock("$app/env/private", () => ({ MAX_REQUESTS_PER_MINUTE: 2 }));

vi.mock("#lib/env.ts", async (importOriginal) => ({
  ...(await importOriginal<typeof import("#lib/env.ts")>()),
  ENVIRONMENT: "local",
}));

vi.mock("#lib/utils/nexus.ts", () => ({
  handleInboundNexusAutoLogin: vi.fn(),
}));

type Handler = (input: {
  event: unknown;
  resolve: (event: unknown) => unknown;
}) => unknown;

vi.mock("@sentry/sveltekit", () => ({
  init: vi.fn(),
  captureException: vi.fn(),
  sentryHandle:
    (): Handler =>
    ({ event, resolve }) =>
      resolve(event),
}));

// Le `sequence` de SvelteKit nécessite le contexte de requête du serveur
vi.mock("@sveltejs/kit/hooks", () => ({
  sequence:
    (...handlers: Handler[]): Handler =>
    ({ event, resolve }) =>
      handlers.reduceRight<(event: unknown) => unknown>(
        (next, handler) => (current) =>
          handler({ event: current, resolve: next }),
        resolve
      )(event),
}));

// Import after mocks are set up
const { handle, handleError } = await import("../hooks.server");
const Sentry = await import("@sentry/sveltekit");

function makeEvent(path: string, clientAddress: string) {
  const url = new URL(`http://localhost${path}`);
  return {
    url,
    request: new Request(url, { headers: { "user-agent": "vitest" } }),
    cookies: { get: () => undefined },
    getClientAddress: () => clientAddress,
  };
}

function callHandle(path: string, clientAddress: string) {
  return handle({
    event: makeEvent(path, clientAddress) as any,
    resolve: () => Promise.resolve(new Response("ok")),
  });
}

describe("rate limiting du front", () => {
  test("limite les pages au-delà du seuil", async () => {
    await callHandle("/", "203.0.113.1");
    await callHandle("/", "203.0.113.1");

    await expect(callHandle("/", "203.0.113.1")).rejects.toMatchObject({
      status: 429,
    });
  });

  test("ne limite pas les appels au proxy /api", async () => {
    const responses = await Promise.all(
      Array.from({ length: 5 }, () =>
        callHandle("/api/services/", "203.0.113.2")
      )
    );

    responses.forEach((response) => expect(response.status).toBe(200));
  });
});

describe("handleError", () => {
  beforeEach(() => {
    vi.mocked(Sentry.captureException).mockClear();
  });

  // Seules les erreurs `unknown` sont inattendues : les autres portent déjà un
  // statut et un message et on les renvoie pas à Sentry.
  test.each(["app", "framework", "validation"] as const)(
    "laisse les defaults de SvelteKit pour kind: %s",
    (kind) => {
      const result = handleError({
        kind,
        error: { status: 404, message: "Not Found" },
        event: makeEvent("/", "203.0.113.3"),
      } as any);

      expect(result).toBeUndefined();
      expect(Sentry.captureException).not.toHaveBeenCalled();
    }
  );

  test("rapporte les erreurs kind: unknown à Sentry", () => {
    const err = new Error("boom");

    const result = handleError({
      kind: "unknown",
      error: err,
      event: makeEvent("/", "203.0.113.3"),
    } as any);

    expect(Sentry.captureException).toHaveBeenCalledWith(err);
    expect(result).toEqual({ message: "boom" });
  });

  // Régression : un `handleError` asynchrone est ignoré par SvelteKit 3 pour les
  // erreurs levées pendant le rendu SSR (cf. commentaire dans `hooks.server.ts`)
  test("reste synchrone", () => {
    const result = handleError({
      kind: "unknown",
      error: new Error("boom"),
      event: makeEvent("/", "203.0.113.3"),
    } as any);

    expect(result).not.toBeInstanceOf(Promise);
  });

  test("masque le message des erreurs non-`Error`", () => {
    const result = handleError({
      kind: "unknown",
      error: "boom",
      event: makeEvent("/", "203.0.113.3"),
    } as any);

    expect(Sentry.captureException).toHaveBeenCalledWith("boom");
    expect(result).toEqual({ message: UNEXPECTED_ERROR_MESSAGE });
  });

  test("masque le message réel hors environnement local", async () => {
    vi.resetModules();
    vi.doMock("#lib/env.ts", async (importOriginal) => ({
      ...(await importOriginal<typeof import("#lib/env.ts")>()),
      ENVIRONMENT: "production",
    }));

    const { handleError: handleErrorInProd } = await import("../hooks.server");

    const result = handleErrorInProd({
      kind: "unknown",
      error: new Error("détail à ne pas exposer"),
      event: makeEvent("/", "203.0.113.3"),
    } as any);

    expect(result).toEqual({ message: UNEXPECTED_ERROR_MESSAGE });
  });
});
