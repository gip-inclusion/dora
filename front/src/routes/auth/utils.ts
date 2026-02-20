export function getNextPage(url: URL) {
  const next = url.searchParams.get("next");
  const basePath = next && next.startsWith("/") ? next : "/";

  // Preserve query params (except "next") from the current URL
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
