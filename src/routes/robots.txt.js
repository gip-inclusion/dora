import { ENVIRONMENT } from "$lib/env.js";

let productionContent = `
User-agent: *
Allow: /
`.trim();

let devContent = `
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
