import { ENVIRONMENT, CANONICAL_URL } from "$lib/env.js";

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
  return {
    status: 200,
    headers: { "content-type": "text/plain" },
    body: content,
  };
}
