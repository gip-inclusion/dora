import { SITEMAP_PAGE_SIZE } from "$lib/consts";
import { CANONICAL_URL } from "$lib/env";
import { getActiveStructures } from "$lib/requests/structures";
import { toISODate } from "$lib/utils/date";

import type { RequestHandler } from "./$types";

async function getUrlEntries(page: number) {
  const structures = await getActiveStructures({
    pageSize: SITEMAP_PAGE_SIZE,
    page: page,
  });

  if (!structures) {
    return "";
  }

  return structures.results
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
  const urlSet = await getUrlSet(Number(params.page));

  return new Response(urlSet, {
    headers: {
      "Content-Type": "application/xml",
    },
  });
};
