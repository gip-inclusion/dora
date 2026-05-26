import type { RequestHandler } from "@sveltejs/kit";
import { API_URL } from "$lib/env";
import { TOKEN_KEY } from "$lib/utils/auth";

async function proxyRequest(event: Parameters<RequestHandler>[0]) {
  const { request, cookies, params } = event;
  const token = cookies.get(TOKEN_KEY);

  const normalizedPath = params.path?.endsWith("/")
    ? params.path
    : `${params.path}/`;
  const targetUrl = `${API_URL}/${normalizedPath}${event.url.search}`;

  const headers = new Headers(request.headers);
  headers.delete("host");
  if (token) {
    headers.set("Authorization", `Token ${token}`);
  }

  const response = await fetch(targetUrl, {
    method: request.method,
    headers,
    body:
      request.method !== "GET" && request.method !== "HEAD"
        ? request.body
        : undefined,
    duplex: "half",
  } as RequestInit);

  const responseHeaders = new Headers(response.headers);
  responseHeaders.delete("set-cookie");

  return new Response(response.body, {
    status: response.status,
    headers: responseHeaders,
  });
}

export const GET: RequestHandler = (event) => proxyRequest(event);
export const POST: RequestHandler = (event) => proxyRequest(event);
export const PUT: RequestHandler = (event) => proxyRequest(event);
export const PATCH: RequestHandler = (event) => proxyRequest(event);
export const DELETE: RequestHandler = (event) => proxyRequest(event);
