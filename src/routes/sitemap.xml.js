import { ENVIRONMENT, CANONICAL_URL } from "$lib/env.js";
import { getServices } from "$lib/services";

async function getContent() {
  const response = await getServices();
  const services = response
    .filter((s) => !s.isDraft)
    .map((s) => {
      const date = new Date(s.modificationDate).toISOString();
      const isoDate = date.slice(0, date.indexOf("T"));

      return `<url>
      <loc>${CANONICAL_URL}/services/${s.slug}</loc>
      <lastmod>${isoDate}</lastmod>
      <priority>0.5</priority>
    </url>`.trim();
    })
    .join("\n");
  const content = `
  <?xml version="1.0" encoding="UTF-8" ?>
    <urlset
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>${CANONICAL_URL}/</loc>
        <priority>1</priority>
      </url>
      ${services}
    </urlset>`.trim();

  return content;
}

export async function get() {
  const content = await getContent();

  if (ENVIRONMENT === "production") {
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
