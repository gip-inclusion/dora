import { error } from "@sveltejs/kit";

import { SITEMAP_PAGE_SIZE } from "$lib/consts";
import { CANONICAL_URL, ENVIRONMENT } from "$lib/env";
import { getActiveStructures } from "$lib/requests/structures";

import type { RequestHandler } from "./$types";

function toISODate(apiDate) {
  const date = new Date(apiDate).toISOString();
  return date.slice(0, date.indexOf("T"));
}

async function getUrlEntries(page: number) {
  const activeStructures = await getActiveStructures({
    pageSize: SITEMAP_PAGE_SIZE,
    page: page,
  });

  if (!activeStructures) {
    return "";
  }

  return activeStructures
    .map(
      (structure) =>
        `<url>
      <loc>${CANONICAL_URL}/structures/${structure.slug}</loc>
      <lastmod>${toISODate(structure.modificationDate)}</lastmod>
      <priority>0.7</priority>
    </url>`
    )
    .join("\n");
}

async function getUrlSet(page: number) {
  return `
  <?xml version="1.0" encoding="UTF-8" ?>
  <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    ${await getUrlEntries(page)}
  </urlset>`.trim();
}

export const GET: RequestHandler = async ({ params }) => {
  if (!["production", "local", "dev"].includes(ENVIRONMENT)) {
    error(404, "Page Not Found");
  }

  const urlSet = await getUrlSet(Number(params.page));

  return new Response(urlSet, {
    headers: {
      "Content-Type": "application/xml",
    },
  });
};
