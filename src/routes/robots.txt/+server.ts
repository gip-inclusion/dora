import { CANONICAL_URL, ENVIRONMENT } from "$lib/env";

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
  return new Response(content, {
    headers: { "content-type": "text/plain" },
  });
}
