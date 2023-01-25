export function getNextPage(url) {
  const next = decodeURIComponent(url.searchParams.get("next"));
  if (next && next.startsWith("/")) {
    return next;
  }
  return "/";
}
