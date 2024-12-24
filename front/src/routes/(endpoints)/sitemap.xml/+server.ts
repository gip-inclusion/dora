import { error } from "@sveltejs/kit";

import { SITEMAP_PAGE_SIZE } from "$lib/consts";
import { CANONICAL_URL, ENVIRONMENT } from "$lib/env";
import { getActiveStructureCount } from "$lib/requests/structures";

async function getStructureSitemaps() {
  const structureCount = await getActiveStructureCount();

  if (structureCount === null) {
    return "";
  }

  const pageCount = Math.ceil(structureCount / SITEMAP_PAGE_SIZE);

  return Array.from({ length: pageCount })
    .map(
      (_item, index) =>
        `<sitemap>
           <loc>${CANONICAL_URL}/sitemap-structures-${index + 1}.xml</loc>
         </sitemap>`
    )
    .join("\n");
}

async function getSitemapIndex() {
  return `
  <?xml version="1.0" encoding="UTF-8" ?>
  <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    ${await getStructureSitemaps()}
  </sitemapindex>`.trim();
}

export async function GET() {
  const sitemapIndex = await getSitemapIndex();
  if (
    ENVIRONMENT === "production" ||
    ENVIRONMENT === "local" ||
    ENVIRONMENT === "dev"
  ) {
    return new Response(sitemapIndex, {
      headers: {
        "Content-Type": "application/xml",
      },
    });
  } else {
    error(404, "Page Not Found");
  }
}
