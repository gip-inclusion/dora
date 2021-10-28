export async function get() {
  return {
    status: 200,
    headers: { "content-type": "text/plain" },
    body: "ok",
  };
}
