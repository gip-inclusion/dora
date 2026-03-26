import fileSystem from "fs";
import v8Engine from "v8";

import { env } from "$env/dynamic/private";

export function GET({ request }: { request: Request }) {
  if (
    !env.SNAPSHOT_SECRET ||
    request.headers.get("x-snapshot-secret") !== env.SNAPSHOT_SECRET
  ) {
    return new Response("forbidden", { status: 403 });
  }

  const filename = `/tmp/heap-${Date.now()}.heapsnapshot`;
  v8Engine.writeHeapSnapshot(filename);
  const snapshot = fileSystem.readFileSync(filename);
  fileSystem.unlinkSync(filename);

  return new Response(snapshot, {
    headers: {
      "content-type": "application/octet-stream",
      "content-disposition": `attachment; filename="heap-${Date.now()}.heapsnapshot"`,
    },
  });
}
