import { error } from "@sveltejs/kit";

import { SITEMAP_PAGE_SIZE } from "$lib/consts";
import { CANONICAL_URL, ENVIRONMENT } from "$lib/env";
import { getPublishedServices } from "$lib/requests/services";
import { getActiveStructures } from "$lib/requests/structures";

async function getServiceSitemaps() {
  const services = await getPublishedServices({ page: 1, pageSize: 1 });

  if (!services) {
    return "";
  }

  const pageCount = Math.ceil(services.count / SITEMAP_PAGE_SIZE);

  return Array.from({ length: pageCount })
    .map(
      (_item, index) =>
        `<sitemap>
           <loc>${CANONICAL_URL}/sitemap-services-${index + 1}.xml</loc>
         </sitemap>`
    )
    .join("\n");
}

async function getStructureSitemaps() {
  const structures = await getActiveStructures({ page: 1, pageSize: 1 });

  if (!structures) {
    return "";
  }

  const pageCount = Math.ceil(structures.count / SITEMAP_PAGE_SIZE);

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
    ${await getServiceSitemaps()}
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
