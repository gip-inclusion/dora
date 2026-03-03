import { goto } from "$app/navigation";
import { redirect } from "@sveltejs/kit";

import { getApiURL } from "./api";
import { getToken } from "$lib/utils/auth";

interface EmploisOrientationParams {
  serviceSlug: string;
  opJwt: string;
}

async function fetchEmploisOrientationNextUrl({
  serviceSlug,
  opJwt,
}: EmploisOrientationParams) {
  const apiUrl = new URL(`/orientations/emplois/${serviceSlug}/`, getApiURL());
  apiUrl.searchParams.set("op", opJwt);

  const token = getToken();
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
    return data.nextUrl || null;
  }

  return null;
}

export async function handleEmploisOrientation(
  params: EmploisOrientationParams
) {
  const nextUrl = await fetchEmploisOrientationNextUrl(params);
  if (nextUrl) {
    await goto(nextUrl);
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
