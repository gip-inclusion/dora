import type { RequestHandler } from "@sveltejs/kit";
import { API_URL, INTERNAL_API_URL } from "$lib/env";
import { TOKEN_KEY } from "$lib/utils/auth";

const apiBase = INTERNAL_API_URL || API_URL;

async function proxyRequest(event: Parameters<RequestHandler>[0]) {
  const { request, cookies, params } = event;
  const token = cookies.get(TOKEN_KEY);

  const targetUrl = `${apiBase}/${params.path}${event.url.search}`;

  const headers = new Headers(request.headers);
  headers.delete("host");
  if (token) {
    headers.set("Authorization", `Token ${token}`);
  }

  const response = await fetch(targetUrl, {
    method: request.method,
    headers,
    body: request.method !== "GET" && request.method !== "HEAD"
      ? await request.arrayBuffer()
      : undefined,
  });

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
