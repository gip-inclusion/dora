import { API_URL } from "$lib/env";
import { disconnect } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";

export const load = () => {
  disconnect();
  redirect(302, API_URL + "/oidc/pre_logout/");
};
