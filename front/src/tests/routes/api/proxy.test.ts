import { beforeEach, describe, expect, test, vi } from "vitest";

vi.mock("$lib/env", () => ({
  API_URL: "http://backend",
}));

vi.mock("$lib/utils/auth", () => ({
  TOKEN_KEY: "token",
}));

const privateEnv: Record<string, string | undefined> = {};
vi.mock("$env/dynamic/private", () => ({ env: privateEnv }));

// Import after mocks are set up
const { GET, POST, PUT, PATCH, DELETE } =
  await import("../../../routes/api/[...path]/+server");

function makeEvent({
  method = "GET",
  path = "services/",
  search = "",
  token = null,
  body = null,
  headers = {},
}: {
  method?: string;
  path?: string;
  search?: string;
  token?: string | null;
  body?: BodyInit | null;
  headers?: Record<string, string>;
} = {}) {
  return {
    request: new Request(`http://localhost/api/${path}${search}`, {
      method,
      headers,
      body: body ?? (method !== "GET" && method !== "HEAD" ? null : undefined),

      duplex: "half",
    } as RequestInit),
    cookies: {
      get: (key: string) =>
        key === "token" ? (token ?? undefined) : undefined,
    },
    params: { path },
    url: new URL(`http://localhost/api/${path}${search}`),
    getClientAddress: () => "203.0.113.7",
  };
}

describe("proxy", () => {
  beforeEach(() => {
    privateEnv.FRONT_PROXY_SECRET = undefined;
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("ok", { status: 200 }))
    );
  });

  test("transmet le token dans le header Authorization", async () => {
    const event = makeEvent({ token: "abc123" });
    await GET(event as any);

    const [, init] = vi.mocked(fetch).mock.calls[0];
    expect(new Headers(init?.headers as HeadersInit).get("Authorization")).toBe(
      "Token abc123"
    );
  });

  test("n'envoie pas de header Authorization sans token", async () => {
    const event = makeEvent({ token: null });
    await GET(event as any);

    const [, init] = vi.mocked(fetch).mock.calls[0];
    expect(new Headers(init?.headers as HeadersInit).has("Authorization")).toBe(
      false
    );
  });

  test("construit l'URL cible correctement", async () => {
    const event = makeEvent({ path: "structures/123/", search: "?foo=bar" });
    await GET(event as any);

    const [url] = vi.mocked(fetch).mock.calls[0];
    expect(url).toBe("http://backend/structures/123/?foo=bar");
  });

  test("ajoute un slash final si absent (requis par Django)", async () => {
    const event = makeEvent({ path: "structures/123", search: "" });
    await POST(event as any);

    const [url] = vi.mocked(fetch).mock.calls[0];
    expect(url).toBe("http://backend/structures/123/");
  });

  test("supprime le header set-cookie de la réponse", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response("ok", {
          status: 200,
          headers: { "set-cookie": "session=abc" },
        })
      )
    );

    const event = makeEvent();
    const response = await GET(event as any);

    expect(response.headers.has("set-cookie")).toBe(false);
  });

  test("transmet le status de la réponse backend", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("not found", { status: 404 }))
    );

    const event = makeEvent();
    const response = await GET(event as any);

    expect(response.status).toBe(404);
  });

  test("transmet le corps pour les requêtes POST", async () => {
    const event = makeEvent({
      method: "POST",
      body: JSON.stringify({ name: "test" }),
    });
    await POST(event as any);

    const [, init] = vi.mocked(fetch).mock.calls[0];
    expect(init?.method).toBe("POST");
    const body = await new Response(init?.body as BodyInit).text();
    expect(body).toBe(JSON.stringify({ name: "test" }));
  });

  test.each([
    ["PUT", PUT],
    ["PATCH", PATCH],
    ["DELETE", DELETE],
  ])("transmet la méthode %s", async (method, handler) => {
    const event = makeEvent({ method });
    await handler(event as any);

    expect(vi.mocked(fetch).mock.calls[0][1]?.method).toBe(method);
  });

  test("n'envoie pas de corps pour les requêtes GET", async () => {
    const event = makeEvent({ method: "GET" });
    await GET(event as any);

    expect(vi.mocked(fetch).mock.calls[0][1]?.body).toBeUndefined();
  });

  test("transmet l'IP du client authentifiée par le secret partagé", async () => {
    privateEnv.FRONT_PROXY_SECRET = "s3cret";
    const event = makeEvent();
    await GET(event as any);

    const headers = new Headers(vi.mocked(fetch).mock.calls[0][1]?.headers);
    expect(headers.get("X-Dora-Client-Ip")).toBe("203.0.113.7");
    expect(headers.get("X-Dora-Proxy-Secret")).toBe("s3cret");
  });

  test("remplace les en-têtes d'IP fournis par le navigateur", async () => {
    const event = makeEvent({
      headers: {
        "X-Forwarded-For": "192.0.2.1",
        "X-Real-IP": "192.0.2.1",
        "X-Dora-Client-Ip": "192.0.2.1",
        "X-Dora-Proxy-Secret": "faux",
      },
    });
    await GET(event as any);

    const headers = new Headers(vi.mocked(fetch).mock.calls[0][1]?.headers);
    expect(headers.get("X-Forwarded-For")).toBe("203.0.113.7");
    expect(headers.has("X-Real-IP")).toBe(false);
    expect(headers.has("X-Dora-Client-Ip")).toBe(false);
    expect(headers.has("X-Dora-Proxy-Secret")).toBe(false);
  });
});
