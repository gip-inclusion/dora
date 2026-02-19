import { redirect } from "@sveltejs/kit";

import { getApiURL } from "./api";

export async function handleEmploisOrientation(url: URL, token?: string) {
  const opJwt = url.searchParams.get("op");

  if (!opJwt) {
    return;
  }

  // Only handle orientation on service detail pages
  const serviceMatch = url.pathname.match(/^\/services\/([^/]+)\/?$/);
  if (!serviceMatch) {
    return;
  }

  const serviceSlug = serviceMatch[1];
  const apiUrl = new URL(`/orientations/emplois/${serviceSlug}/`, getApiURL());
  apiUrl.searchParams.set("op", opJwt);

  const response = await fetch(apiUrl, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      ...(token && { Authorization: `Token ${token}` }),
    },
  });

  if (response.ok) {
    const data = await response.json();
    if (data.nextUrl) {
      redirect(302, data.nextUrl);
    }
  }
}

export async function handleNexusAutoLogin(url: URL, token?: string) {
  const autoLoginJwt = url.searchParams.get("auto_login");

  if (!autoLoginJwt) {
    return;
  }

  const autoLoginUrl = new URL("/nexus/auto-login-in/", getApiURL());

  url.searchParams.delete("auto_login");

  const response = await fetch(autoLoginUrl, {
    method: "POST",
    body: JSON.stringify({
      jwt: autoLoginJwt,
      next: url.toString(),
    }),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      ...(token && { Authorization: `Token ${token}` }),
    },
  });

  if (response.status === 204) {
    return;
  }

  if (response.ok) {
    const data = await response.json();
    if (data.redirectUrl) {
      redirect(302, data.redirectUrl);
    }
  }
}
