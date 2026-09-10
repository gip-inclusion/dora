export const enum LocationType {
  Address,
  City,
  Department,
  Region,
  EPCI,
}

export interface LocationValue {
  type: LocationType;
  // code INSEE pour une commune, codes de départements pour les autres types
  codes: string[];
}

// Le Select compare ses valeurs par identité : on utilise une clé stable, et
// non un objet, pour qu'une même localisation reste reconnue d'une recherche
// à l'autre.
export interface LocationOption {
  value: string;
  label: string;
}

const LOCATION_KEY_SEPARATOR = "|";

export function serializeLocation({ type, codes }: LocationValue): string {
  return `${type}${LOCATION_KEY_SEPARATOR}${codes.join(",")}`;
}

export function parseLocation(key: string): LocationValue {
  const [type, codes] = key.split(LOCATION_KEY_SEPARATOR);
  return {
    type: Number(type) as LocationType,
    codes: codes ? codes.split(",") : [],
  };
}

export interface AddressResult {
  kind: LocationType;
  label: string;
  searchParams: URLSearchParams;
}

export const TEXT_SEARCH_LAST_LOCATION_STORAGE_KEY = "lastSelectedLocation";

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
      searchParams: new URLSearchParams(parsed.searchParams),
    };
  } catch {
    return null;
  }
}

export function saveLastLocation(newAddress: AddressResult | null) {
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
        searchParams: newAddress.searchParams.toString(),
      })
    );
  } catch {
    // Le localStorage peut être inaccessible.
  }
}
