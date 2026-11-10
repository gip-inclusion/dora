import { describe, expect, test, vi } from "vitest";

vi.mock("$env/static/private", () => ({ MAX_REQUESTS_PER_MINUTE: "2" }));

vi.mock("$lib/env", async (importOriginal) => ({
  ...(await importOriginal<typeof import("$lib/env")>()),
  ENVIRONMENT: "local",
}));

vi.mock("$lib/utils/nexus", () => ({
  handleInboundNexusAutoLogin: vi.fn(),
}));

type Handler = (input: {
  event: unknown;
  resolve: (event: unknown) => unknown;
}) => unknown;

vi.mock("@sentry/sveltekit", () => ({
  init: vi.fn(),
  handleErrorWithSentry: vi.fn(),
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
const { handle } = await import("../hooks.server");

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
