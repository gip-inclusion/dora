import { getApiURL } from "$lib/utils/api";
import { error, redirect } from "@sveltejs/kit";
import type { RequestEvent } from "@sveltejs/kit";

export const load = async ({ cookies, url }: RequestEvent) => {
  const token = cookies.get("token") ?? null;

  const nextUrl = url.searchParams.get("next");

  if (!token || !nextUrl) {
    error(404, "Page Not Found");
  }

  const autoLoginUrl = new URL("/nexus/auto-login-out/", getApiURL());

  const response = await fetch(autoLoginUrl, {
    method: "POST",
    body: JSON.stringify({
      nextUrl,
    }),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      Authorization: `Token ${token}`,
    },
  });

  if (response.ok) {
    const data = await response.json();
    if (data.redirectUrl) {
      redirect(302, data.redirectUrl);
    }
  }

  error(404, "Page Not Found");
};
