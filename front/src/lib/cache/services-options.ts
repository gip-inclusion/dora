import type { ServicesOptions } from "$lib/types";
import type { UserInfo } from "$lib/utils/auth";

// Les servicesOptions peuvent varier en fonction du statut d'authentification,
// des structures rattachées, des départements et du rôle de l'utilisateur.
// On a ces informations dans le userInfo. On les conserve dans le userContext
// pour savoir si on doit invalider le cache.
interface UserContext {
  isAuthenticated: boolean;
  structures: string[];
  departments: string[];
  isStaff: boolean;
  isManager: boolean;
}

// Le cache contient les données servicesOptions et les informations
// qui servent à l'invalider : le timestamp et le userContext.
interface CacheEntry {
  data: ServicesOptions;
  timestamp: number;
  userContext: UserContext;
}

// Cache valide pendant 1 heure.
const CACHE_DURATION = 1 * 60 * 60 * 1000;

let cache: CacheEntry | null = null;

// Crée le userContext à partir du userInfo
function createUserContext(userInfo: UserInfo | null): UserContext {
  if (!userInfo) {
    return {
      isAuthenticated: false,
      structures: [],
      departments: [],
      isStaff: false,
      isManager: false,
    };
  }

  return {
    isAuthenticated: true,
    structures: userInfo.structures.map((structure) => structure.slug),
    departments: userInfo.departments,
    isStaff: userInfo.isStaff,
    isManager: userInfo.isManager,
  };
}

// Vérifie si le userContext a changé
function hasUserContextChanged(currentContext: UserContext): boolean {
  if (!cache) {
    return true;
  }

  return JSON.stringify(currentContext) !== JSON.stringify(cache.userContext);
}

// Cache simple pour les servicesOptions
// Évite les appels API répétés pendant la durée de validité du cache
// Invalide automatiquement si le contexte utilisateur change
export function getCachedServicesOptions(
  userInfo: UserInfo | null = null
): ServicesOptions | null {
  // Pas de cache -> on retourne null
  if (!cache) {
    return null;
  }

  const now = Date.now();
  // Cache expiré -> cache invalide -> on retourne null
  if (now - cache.timestamp > CACHE_DURATION) {
    cache = null;
    return null;
  }

  // userContext a changé -> cache invalide -> on retourne null
  const currentContext = createUserContext(userInfo);
  if (hasUserContextChanged(currentContext)) {
    cache = null;
    return null;
  }

  // Cache présent et valide -> on retourne les données cachées
  return cache.data;
}

// Met à jour le cache avec de nouvelles données
export function setCachedServicesOptions(
  data: ServicesOptions,
  userInfo: UserInfo | null = null
): void {
  const userContext = createUserContext(userInfo);

  // On met à jour le cache avec les nouvelles données, le timestamp et le userContext à jour
  cache = {
    data,
    timestamp: Date.now(),
    userContext,
  };
}

// Force l'invalidation du cache
export function invalidateServicesOptionsCache(): void {
  cache = null;
}
