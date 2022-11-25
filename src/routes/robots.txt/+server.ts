import { CANONICAL_URL, ENVIRONMENT } from "$lib/env";
import { json } from "@sveltejs/kit";

const productionContent = `
User-agent: *
Disallow: /mon-compte/
Disallow: /auth/
Sitemap: ${CANONICAL_URL}/sitemap.xml
`.trim();

const devContent = `
User-agent: *
Disallow: /
`.trim();

const content = ENVIRONMENT === "production" ? productionContent : devContent;

export async function GET() {
  return json(content, {
    headers: { "content-type": "text/plain" },
  });
}
