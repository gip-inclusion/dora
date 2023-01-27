export function GET() {
  return new Response("ok", { headers: { "content-type": "text/plain" } });
}
