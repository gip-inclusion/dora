import { ENVIRONMENT } from "$lib/env.js";

const productionContent = `
User-agent: *
Allow: /
`.trim();

const devContent = `
User-agent: *
Disallow: /
`.trim();

const content = ENVIRONMENT === "production" ? productionContent : devContent;

export async function get() {
  return {
    status: 200,
    headers: { "content-type": "text/plain" },
    body: content,
  };
}
