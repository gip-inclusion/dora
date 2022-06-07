import showdown from "showdown";
import insane from "insane";
import { get } from "svelte/store";

import { browser } from "$app/env";

import { token } from "$lib/auth";
import { defaultAcceptHeader } from "$lib/utils/api";

export function markdownToHTML(md) {
  const converter = new showdown.Converter({
    extensions: [
      () => ({
        type: "output",
        filter(html) {
          return html.replaceAll("<a href=", '<a rel="nofollow" href=');
        },
      }),
    ],
  });

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
  { acceptHeader = defaultAcceptHeader, kitFetch } = {}
) {
  const headers = { Accept: acceptHeader };
  const tk = get(token);

  if (tk) {
    headers.Authorization = `Token ${tk}`;
  }

  const response = await (kitFetch || fetch)(url, {
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

export function shortenString(str, length = 50) {
  if (str && str.length > length) {
    return `${str.slice(0, length)}…`;
  }

  return str;
}

export function capitalize(str) {
  return str.toLowerCase().replace(/\b\w/gu, (c) => c.toUpperCase());
}

export function getDepartmentFromCityCode(cityCode) {
  if (cityCode == null) {
    return null;
  }

  return cityCode.startsWith("97")
    ? cityCode.slice(0, 3)
    : cityCode.slice(0, 2);
}

export function addlinkToUrls(text) {
  const urlRegex = /((https?|mailto):\/\/[^\s]+\.[^\s]+)/gu;

  return insane(
    text.replace(
      urlRegex,
      (url) =>
        `<a href="${url}" class="underline" rel="noopener nofollow">${url}</a>`
    ),
    { allowedTags: ["a"], allowedAttributes: { a: ["class", "rel", "href"] } }
  );
}

export function moveToTheEnd(
  array,
  key,
  value,
  sortBeginning = false,
  sortKey = "label"
) {
  const elementsToMove = array.filter((e) => e[key] === value);

  if (!elementsToMove.length) {
    return array;
  }

  let beginning = array.filter((e) => e[key] !== value);
  if (sortBeginning) {
    beginning = beginning.sort((a, b) =>
      a[sortKey].localeCompare(b[sortKey], "fr", { numeric: true })
    );
  }

  return [...beginning, ...elementsToMove];
}
