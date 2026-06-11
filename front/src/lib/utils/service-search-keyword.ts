export const enum LocationType {
  Address,
  City,
  Department,
  Region,
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
