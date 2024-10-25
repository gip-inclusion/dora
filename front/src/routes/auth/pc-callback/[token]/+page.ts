import { CANONICAL_URL } from "$lib/env";
import { setToken } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";
import { getNextPage } from "../../utils";

export const load = ({ params, url }) => {
  const token = params.token;
  setToken(token);

  const nextPage = getNextPage(url);
  url.searchParams.delete("next");
  const qsParams = url.searchParams.toString();
  const uri = nextPage + (qsParams !== "" ? "&" + qsParams : "");

  redirect(302, CANONICAL_URL + uri);
};
