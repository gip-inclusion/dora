import { browser } from "$app/env";
import showdown from "showdown";

import { API_URL, INTERNAL_API_URL } from "$lib/env.js";

export function getApiURL() {
  if (browser || !INTERNAL_API_URL) return API_URL;
  return INTERNAL_API_URL;
}

export function markdownToHTML(md) {
  const converter = new showdown.Converter();
  return converter.makeHtml(md);
}

export function htmlToMarkdown(html) {
  if (browser) {
    const converter = new showdown.Converter();
    return converter.makeMarkdown(html);
  }
  return "";
}

export async function fetchData(
  url,
  { acceptHeader = "application/json; version=1.0" } = {}
) {
  const response = await fetch(url, {
    headers: {
      Accept: acceptHeader,
    },
  });

  if (!response.ok) {
    throw Error(response.statusText);
  }

  return await response.json();
}
