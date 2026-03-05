export function getNextPage(url: URL) {
  const next = url.searchParams.get("next");
  if (next && next.startsWith("/")) {
    return next;
  }
  return "/";
}