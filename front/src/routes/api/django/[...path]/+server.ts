import type { RequestHandler } from "./$types";
import { API_URL } from "$lib/env";

async function proxyToDjango(
  method: string,
  path: string,
  request: Request,
  getClientAddress: () => string,
  searchParams: URLSearchParams
) {
  const clientIP = getClientAddress();

  const formattedPath = path.endsWith("/") ? path : `${path}/`;

  const djangoUrl = `${API_URL}/${formattedPath}${searchParams.toString() ? "?" + searchParams.toString() : ""}`;

  const headers = new Headers(request.headers);
  headers.set("X-Forwarded-For", clientIP);

  const options: RequestInit = {
    method,
    headers,
  };

  if (["POST", "PUT", "PATCH"].includes(method)) {
    options.body = await request.text();
  }

  const response = await fetch(djangoUrl, options);

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers,
  });
}

export const GET: RequestHandler = ({
  params,
  request,
  getClientAddress,
  url,
}) => {
  return proxyToDjango(
    "GET",
    params.path,
    request,
    getClientAddress,
    url.searchParams
  );
};

export const POST: RequestHandler = ({
  params,
  request,
  getClientAddress,
  url,
}) => {
  return proxyToDjango(
    "POST",
    params.path,
    request,
    getClientAddress,
    url.searchParams
  );
};

export const PUT: RequestHandler = ({
  params,
  request,
  getClientAddress,
  url,
}) => {
  return proxyToDjango(
    "PUT",
    params.path,
    request,
    getClientAddress,
    url.searchParams
  );
};

export const DELETE: RequestHandler = ({
  params,
  request,
  getClientAddress,
  url,
}) => {
  return proxyToDjango(
    "DELETE",
    params.path,
    request,
    getClientAddress,
    url.searchParams
  );
};

export const PATCH: RequestHandler = ({
  params,
  request,
  getClientAddress,
  url,
}) => {
  return proxyToDjango(
    "PATCH",
    params.path,
    request,
    getClientAddress,
    url.searchParams
  );
};
