import { CANONICAL_URL } from "$lib/env";
import { redirect } from "@sveltejs/kit";
import { getNextPage } from "../utils";
import { ORIENTATION_JWT_QUERY_PARAM } from "$lib/consts";

export const load = ({ url }) => {
  const nextPage = getNextPage(url);
  url.searchParams.delete("next");

  const qsParams = url.searchParams.toString();

  const nextPageUrl = new URL(nextPage, CANONICAL_URL);

  if (
    (url.searchParams.has("siret") || url.searchParams.has("safir")) &&
    !nextPageUrl.searchParams.has(ORIENTATION_JWT_QUERY_PARAM)
  ) {
    // Lors de l'identification OIDC côté backend, il a été demandé
    // de proposer à l'utilisateur le rattachement vers une structure
    // ou une agence France Travail spécifique
    // (cas des nouveaux utilisateurs ou sans invitation / rattachement).
    // Dans ce cas uniquement, on ne tiens pas compte du `next`,
    // et on redirige vers la page de rattachement.
    redirect(302, `${CANONICAL_URL}/auth/rattachement?${qsParams}`);
  }

  const uri = nextPage + (qsParams !== "" ? "&" + qsParams : "");

  redirect(302, CANONICAL_URL + uri);
};
