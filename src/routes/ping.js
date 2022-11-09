export async function GET() {
  return {
    status: 200,
    headers: { "content-type": "text/plain" },
    body: "ok",
  };
}
