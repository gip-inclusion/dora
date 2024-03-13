import { CANONICAL_URL, ENVIRONMENT } from "$lib/env";
import { getPublishedServices } from "$lib/requests/services";
import { getActiveStructures } from "$lib/requests/structures";
import { error } from "@sveltejs/kit";

function toISODate(apiDate) {
  const date = new Date(apiDate).toISOString();
  return date.slice(0, date.indexOf("T"));
}

async function getServicesEntries() {
  const response = await getPublishedServices();

  return response
    .filter((service) => (service.status = "PUBLISHED")) // Pas indispensable, mais c'est une sécurité supplémentaire
    .map((service) =>
      `<url>
      <loc>${CANONICAL_URL}/services/${service.slug}</loc>
      <lastmod>${toISODate(service.modificationDate)}</lastmod>
      <priority>0.5</priority>
    </url>`.trim()
    )
    .join("\n");
}

async function getStructuresEntries() {
  const response = await getActiveStructures();
  return response
    .map((structure) =>
      `<url>
      <loc>${CANONICAL_URL}/structures/${structure.slug}</loc>
      <lastmod>${toISODate(structure.modificationDate)}</lastmod>
      <priority>0.7</priority>
    </url>`.trim()
    )
    .join("\n");
}

function getStaticEntries() {
  return ["contribuer"]
    .map((entry) =>
      `<url>
    <loc>${CANONICAL_URL}/${entry}</loc>
    <priority>1</priority>
  </url>`.trim()
    )
    .join("\n");
}

async function getContent() {
  const content = `
  <?xml version="1.0" encoding="UTF-8" ?>
    <urlset
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>${CANONICAL_URL}/</loc>
        <priority>1</priority>
      </url>
      ${await getStructuresEntries()}
      ${await getServicesEntries()}
      ${getStaticEntries()}
    </urlset>`.trim();

  return content;
}

export async function GET() {
  const content = await getContent();
  if (ENVIRONMENT === "production" || ENVIRONMENT === "local") {
    return new Response(content, {
      headers: {
        "Content-Type": "application/xml",
      },
    });
  } else {
    error(404, "Page Not Found");
  }
}
