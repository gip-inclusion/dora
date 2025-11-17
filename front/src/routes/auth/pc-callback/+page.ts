import { CANONICAL_URL } from "$lib/env";
import { setToken } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";
import { getNextPage } from "../utils";

export const load = ({ url }) => {
  const hash = window.location.hash;
  const token = hash.split("=")[1];

  setToken(token);

  const nextPage = getNextPage(url);
  url.searchParams.delete("next");

  const qsParams = url.searchParams.toString();

  if (url.searchParams.has("siret") || url.searchParams.has("safir")) {
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
