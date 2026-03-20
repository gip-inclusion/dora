import { ORIENTATION_JWT_QUERY_PARAM } from "$lib/consts";

export function doesUrlHaveOrientationJwt(url: URL): boolean {
  if (url.searchParams.has(ORIENTATION_JWT_QUERY_PARAM)) {
    return true;
  }
  const nextParam = url.searchParams.get("next");
  if (nextParam) {
    const nextUrl = new URL(nextParam, url.origin);
    return nextUrl.searchParams.has(ORIENTATION_JWT_QUERY_PARAM);
  }
  return false;
}

export function getNextPage(url: URL) {
  const next = url.searchParams.get("next");
  const basePath = next && next.startsWith("/") ? next : "/";

  // Préserver les query params (sauf "next") dans l'url renvoyé
  const paramsToForward = new URLSearchParams();
  for (const [key, value] of url.searchParams) {
    if (key !== "next") {
      paramsToForward.set(key, value);
    }
  }

  if (paramsToForward.size === 0) {
    return basePath;
  }

  const separator = basePath.includes("?") ? "&" : "?";
  return `${basePath}${separator}${paramsToForward.toString()}`;
}
