import type { SearchQuery } from "#lib/types.ts";
import { logException } from "./logger";
import { LocationType, type AddressResult } from "./service-search-keyword";

const LAST_SEARCH_CITY_KEY = "lastSearch";
const TEXT_SEARCH_LAST_LOCATION_STORAGE_KEY = "lastSelectedLocation";

export function getQueryString({
  categoryIds,
  subCategoryIds,
  cityCode,
  cityLabel,
  label,
  feeConditions,
  fundingLabels,
  locationKinds,
  kindIds,
  lon,
  lat,
}: SearchQuery) {
  const parameters = {
    cats: categoryIds.join(","),
    subs: subCategoryIds.sort().join(","),
    city: cityCode,
    // eslint-disable-next-line id-length
    cl: cityLabel,
    // eslint-disable-next-line id-length
    l: label,
    kinds: kindIds.join(","),
    fees: feeConditions.join(","),
    locs: locationKinds.join(","),
    funding: fundingLabels.join(","),
    lat: lat,
    lon: lon,
  };
  const query = Object.entries(parameters)
    .filter(([_key, value]) => !!value)
    .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
    .join("&");
  return query;
}

export function loadLastLocation(): AddressResult | null {
  try {
    const stored = localStorage.getItem(TEXT_SEARCH_LAST_LOCATION_STORAGE_KEY);
    if (!stored) {
      return null;
    }
    const parsed = JSON.parse(stored);
    return {
      kind: parsed.kind,
      label: parsed.label,
      cityLabel: parsed.cityLabel,
      searchParams: new URLSearchParams(parsed.searchParams),
    };
  } catch {
    return null;
  }
}

function saveLastLocation(newAddress: AddressResult | null) {
  if (newAddress === null) {
    try {
      localStorage.removeItem(TEXT_SEARCH_LAST_LOCATION_STORAGE_KEY);
    } catch {
      // Le localStorage peut être inaccessible.
    }
    return;
  }

  try {
    localStorage.setItem(
      TEXT_SEARCH_LAST_LOCATION_STORAGE_KEY,
      JSON.stringify({
        kind: newAddress.kind,
        label: newAddress.label,
        cityLabel: newAddress.cityLabel,
        searchParams: newAddress.searchParams.toString(),
      })
    );
  } catch {
    // Le localStorage peut être inaccessible.
  }
}

interface LastSearchLocation {
  cityCode: string;
  cityLabel: string;
  // adresse précise : libellé complet et coordonnées
  label?: string;
  lon?: string;
  lat?: string;
}

function writeLastSearchLocation(location: LastSearchLocation) {
  try {
    localStorage.setItem(LAST_SEARCH_CITY_KEY, JSON.stringify(location));
  } catch {
    // Le localStorage peut être inaccessible.
  }
}

// Le dernier lieu (commune ou adresse) est partagé entre la recherche
// thématique et la recherche par mots-clés : chaque enregistrement met à jour
// la mémoire des deux recherches.
export function storeLastSearchLocation(location: LastSearchLocation) {
  writeLastSearchLocation(location);
  const { cityCode, cityLabel, label, lon, lat } = location;
  if (lon && lat) {
    saveLastLocation({
      kind: LocationType.Address,
      label: label || cityLabel,
      cityLabel,
      // eslint-disable-next-line camelcase
      searchParams: new URLSearchParams({ lon, lat, code_insee: cityCode }),
    });
  } else {
    saveLastLocation({
      kind: LocationType.City,
      label: cityLabel,
      // eslint-disable-next-line camelcase
      searchParams: new URLSearchParams({ code_commune: cityCode }),
    });
  }
}

function toThematicSearchLocation(
  location: AddressResult
): LastSearchLocation | null {
  const { kind, label, searchParams } = location;
  if (kind === LocationType.City) {
    const cityCode = searchParams.get("code_commune");
    return cityCode ? { cityCode, cityLabel: label } : null;
  }
  if (kind === LocationType.Address) {
    const cityCode = searchParams.get("code_insee");
    const lon = searchParams.get("lon");
    const lat = searchParams.get("lat");
    // `cityLabel` absent des adresses mémorisées avant le partage du lieu
    if (cityCode && location.cityLabel && lon && lat) {
      return { cityCode, cityLabel: location.cityLabel, label, lon, lat };
    }
  }
  return null;
}

// La recherche thématique ne gère que les communes et les adresses : après le
// choix d'un département ou d'une région, son lieu est vidé plutôt que de
// laisser un lieu plus ancien.
export function storeLastKeywordSearchLocation(location: AddressResult | null) {
  saveLastLocation(location);
  if (!location) {
    return;
  }
  const thematicLocation = toThematicSearchLocation(location);
  if (thematicLocation) {
    writeLastSearchLocation(thematicLocation);
  } else {
    try {
      localStorage.removeItem(LAST_SEARCH_CITY_KEY);
    } catch {
      // Le localStorage peut être inaccessible.
    }
  }
}

export function getLastSearchLocation(): Partial<LastSearchLocation> {
  let location: Partial<LastSearchLocation> = {};
  let lastSearch: string | null = null;
  try {
    lastSearch = localStorage.getItem(LAST_SEARCH_CITY_KEY);
  } catch {
    // Le localStorage peut être inaccessible.
  }
  if (lastSearch) {
    try {
      const { cityCode, cityLabel, label, lon, lat } = JSON.parse(lastSearch);
      location = { cityCode, cityLabel, label, lon, lat };
    } catch (err) {
      logException(err, "Impossible de lire la dernière ville de recherche");
    }
  }
  return location;
}
