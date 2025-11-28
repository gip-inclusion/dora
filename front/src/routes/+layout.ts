import { browser } from "$app/environment";
import { userInfo, validateCredsAndFillUserInfo } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { LayoutLoad } from "./$types";
import { needToAcceptCgu } from "$lib/utils/cgu";
import { handleNexusAutoLogin } from "$lib/utils/nexus";

export const prerender = false;

// Un utilisateur connecté mais rattaché à aucune structure peut quand même acceder aux
// urls suivantes
const SAFE_URLS = [
  "/auth/rattachement",
  "/auth/invitation",
  "/auth/deconnexion",
  "/accessibilite",
  "/cgu",
  "/mentions-legales",
  "/nos-partenaires",
  "/politique-de-confidentialite",
];

export const load: LayoutLoad = async ({ url }) => {
  if (!browser) {
    // On ne fait pas d'authentification coté serveur
    // => on peut court-circuiter les vérifications ici
    return {};
  }

  await handleNexusAutoLogin(url);

  let currentUserInfo = get(userInfo);
  if (!currentUserInfo) {
    await validateCredsAndFillUserInfo();
    currentUserInfo = get(userInfo);
  }

  if (currentUserInfo) {
    // ⚠ Il est nécessaire d'acceder à url.pathname ici pour que cette fonction `load`
    // soit rappelée quand l'URL change, sans quoi SvelteKit optimise l'appel.
    // Voir: https://kit.svelte.dev/docs/load#rerunning-load-functions
    // Or on veut vérifier le token à chaque changement de page, quand l'utilisateur est
    // connecté.
    const currentPathName = url.pathname;

    if (SAFE_URLS.some((urlPrefix) => currentPathName.startsWith(urlPrefix))) {
      return {};
    }

    // Si l'utilisateur est connecté mais n'est rattaché à aucune structure,
    // on le force à se rattacher
    if (
      !(
        currentUserInfo.structures.length ||
        currentUserInfo.pendingStructures.length
      )
    ) {
      redirect(302, `/auth/rattachement${url.search}`);
    }

    // Si l'utilisateur a besoin de valider les CGU en cours de validité
    const userNeedsToAcceptCgu = needToAcceptCgu(currentUserInfo);

    if (
      currentPathName.startsWith("/cgu/validation") &&
      !userNeedsToAcceptCgu
    ) {
      redirect(302, "/");
    }

    if (
      userNeedsToAcceptCgu &&
      !currentPathName.startsWith("/cgu/validation")
    ) {
      redirect(
        302,
        `/cgu/validation?next=${encodeURIComponent(url.pathname + url.search)}`
      );
    }
  }

  return {};
};
