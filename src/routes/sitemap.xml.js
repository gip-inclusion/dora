import { ENVIRONMENT, CANONICAL_URL } from "$lib/env.js";
import { SERVICE_STATUSES } from "$lib/schemas/service";
import { getPublishedServices } from "$lib/services";
import { getStructures } from "$lib/structures";

function toISODate(apiDate) {
  const date = new Date(apiDate).toISOString();
  return date.slice(0, date.indexOf("T"));
}

async function getAllServices() {
  const response = await getPublishedServices();

  return response
    .filter((s) => (s.status = SERVICE_STATUSES.published)) // Pas indispensable, mais c'est une sécurité supplémentaire
    .map((s) =>
      `<url>
      <loc>${CANONICAL_URL}/services/${s.slug}</loc>
      <lastmod>${toISODate(s.modificationDate)}</lastmod>
      <priority>0.5</priority>
    </url>`.trim()
    )
    .join("\n");
}

async function getAllStructures() {
  const response = await getStructures();
  return response
    .map((s) =>
      `<url>
      <loc>${CANONICAL_URL}/structures/${s.slug}</loc>
      <lastmod>${toISODate(s.modificationDate)}</lastmod>
      <priority>0.7</priority>
    </url>`.trim()
    )
    .join("\n");
}

async function getContent() {
  const services = await getAllServices();
  const structures = await getAllStructures();
  const content = `
  <?xml version="1.0" encoding="UTF-8" ?>
    <urlset
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>${CANONICAL_URL}/</loc>
        <priority>1</priority>
      </url>
      ${structures}
      ${services}
    </urlset>`.trim();

  return content;
}

export async function GET() {
  const content = await getContent();
  if (ENVIRONMENT === "production" || ENVIRONMENT === "local") {
    return {
      status: 200,
      headers: {
        "Content-Type": "application/xml",
      },
      body: content,
    };
  }
  return null;
}
