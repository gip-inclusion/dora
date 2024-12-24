import { error } from "@sveltejs/kit";

import { SITEMAP_PAGE_SIZE } from "$lib/consts";
import { CANONICAL_URL, ENVIRONMENT } from "$lib/env";
import { getPublishedServices } from "$lib/requests/services";
import { toISODate } from "$lib/utils/date";

import type { RequestHandler } from "./$types";

async function getUrlEntries(page: number) {
  const services = await getPublishedServices({
    pageSize: SITEMAP_PAGE_SIZE,
    page: page,
  });

  if (!services) {
    return "";
  }

  return services.results
    .map(
      (service) =>
        `<url>
      <loc>${CANONICAL_URL}/services/${service.slug}</loc>
      <lastmod>${toISODate(service.modificationDate)}</lastmod>
      <priority>0.5</priority>
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
