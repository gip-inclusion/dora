import { CANONICAL_URL } from "$lib/env";
import { setToken } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";
import { getNextPage } from "../../utils";

export const load = ({ params, url }) => {
  const token = params.token;
  setToken(token);

  // home pour l'instant
  redirect(302, CANONICAL_URL + getNextPage(url));
};
