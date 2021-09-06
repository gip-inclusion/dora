import showdown from "showdown";

import { get } from "svelte/store";

import { browser } from "$app/env";

import { token } from "$lib/auth";

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
  const headers = {
    Accept: acceptHeader,
  };
  const tk = get(token);
  if (tk) {
    headers.Authorization = `Token ${tk}`;
  }
  const response = await fetch(url, {
    headers,
  });

  return {
    ok: response.ok,
    data: response.ok ? await response.json() : null,
    error: response.ok ? null : await response.json(),
    status: response.status,
    statusText: response.statusText,
  };
}
