import { getApiURL } from "$lib/utils/api";
import { disconnect } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";

export const load = () => {
  disconnect();
  redirect(302, getApiURL() + "/oidc/pre_logout/");
};
