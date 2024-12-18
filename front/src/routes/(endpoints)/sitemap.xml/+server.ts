import { CANONICAL_URL, ENVIRONMENT } from "$lib/env";
import { error } from "@sveltejs/kit";

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

function getContent() {
  const content = `
  <?xml version="1.0" encoding="UTF-8" ?>
    <urlset
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>${CANONICAL_URL}/</loc>
        <priority>1</priority>
      </url>
      ${getStaticEntries()}
    </urlset>`.trim();

  return content;
}

export function GET() {
  const content = getContent();
  if (
    ENVIRONMENT === "production" ||
    ENVIRONMENT === "local" ||
    ENVIRONMENT === "dev"
  ) {
    return new Response(content, {
      headers: {
        "Content-Type": "application/xml",
      },
    });
  } else {
    error(404, "Page Not Found");
  }
}
