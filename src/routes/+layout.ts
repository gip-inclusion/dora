import { browser } from "$app/environment";
import {
  disconnect,
  userInfo,
  validateCredsAndFillUserInfo,
} from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";
import dayjs from "dayjs";
import { get } from "svelte/store";
import type { LayoutLoad } from "./$types";

export const prerender = false;

function tokenWillExpireSoon(tokenExpirationString: string): boolean {
  const tokenExpirationDate = dayjs(tokenExpirationString);
  if (!tokenExpirationDate.isValid()) {
    // Impossible de parser la date d'expiration -- on considère que
    // le token est invalide
    return true;
  }
  const minimalValidityDate = dayjs().add(1, "days");
  return tokenExpirationDate.isBefore(minimalValidityDate);
}

export const load: LayoutLoad = async ({ url }) => {
  if (!browser) {
    // On ne fait pas d'authentification coté serveur
    // => on peut court-circuiter les vérifications ici
    return {};
  }

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

    // Si l'utilisateur est connecté, mais que son token expire dans moins de 24h,
    // on force une deconnexion, afin qu'il récupère un token frais dès qu'il en aura besoin.
    if (tokenWillExpireSoon(currentUserInfo.tokenExpiration)) {
      // logout and reload page
      disconnect();
      window.location.reload();
      return {};
    }

    // Si l'utilisateur est connecté mais n'est rattaché à aucune structure,
    // on le force à se rattacher
    if (
      !(
        currentUserInfo.structures.length ||
        currentUserInfo.pendingStructures.length
      ) &&
      !currentPathName.startsWith("/auth/rattachement") &&
      !currentPathName.startsWith("/auth/invitation") &&
      !currentPathName.startsWith("/auth/deconnexion")
    ) {
      throw redirect(302, "/auth/rattachement");
    }
  }

  return {};
};
