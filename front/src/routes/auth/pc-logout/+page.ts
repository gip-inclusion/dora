import { API_URL } from "#lib/env.ts";
import { disconnect } from "#lib/utils/auth.ts";
import { redirect } from "@sveltejs/kit";

export const load = async () => {
  await disconnect();
  redirect(302, `${API_URL}/oidc/pre_logout/`);
};
