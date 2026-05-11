import type { RequestHandler } from "@sveltejs/kit";
import { AUTH_STATE_KEY, TOKEN_KEY } from "$lib/utils/auth";

export const POST: RequestHandler = ({ cookies }) => {
  cookies.delete(TOKEN_KEY, { path: "/" });
  cookies.delete(AUTH_STATE_KEY, { path: "/" });
  return new Response(null, { status: 204 });
};
