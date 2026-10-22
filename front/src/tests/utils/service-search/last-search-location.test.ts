/* eslint-disable camelcase -- query params conservés en snake_case */
import { beforeEach, describe, expect, test, vi } from "vitest";

import {
  getLastSearchLocation,
  storeLastKeywordSearchLocation,
  storeLastSearchLocation,
} from "$lib/utils/service-search";
import {
  LocationType,
  loadLastLocation,
} from "$lib/utils/service-search-keyword";

beforeEach(() => {
  const store = new Map<string, string>();
  vi.stubGlobal("localStorage", {
    getItem: (key: string) => store.get(key) ?? null,
    setItem: (key: string, value: string) => store.set(key, value),
    removeItem: (key: string) => store.delete(key),
  });
});

const BORDEAUX_ADDRESS = {
  cityCode: "33063",
  cityLabel: "Bordeaux (33)",
  label: "1 Rue de l’Espoir 33000 Bordeaux",
  lon: "-0.57",
  lat: "44.83",
};

describe("last search location", () => {
  test("a thematic search city is reused by the keyword search", () => {
    storeLastSearchLocation({ cityCode: "69123", cityLabel: "Lyon (69)" });

    const location = loadLastLocation();
    expect(location?.kind).toBe(LocationType.City);
    expect(location?.label).toBe("Lyon (69)");
    expect(location?.searchParams.toString()).toBe("code_commune=69123");
  });

  test("a thematic search address is reused by the keyword search", () => {
    storeLastSearchLocation(BORDEAUX_ADDRESS);

    const location = loadLastLocation();
    expect(location?.kind).toBe(LocationType.Address);
    expect(location?.label).toBe(BORDEAUX_ADDRESS.label);
    expect(location?.cityLabel).toBe("Bordeaux (33)");
    expect(Object.fromEntries(location?.searchParams ?? [])).toEqual({
      lon: "-0.57",
      lat: "44.83",
      code_insee: "33063",
    });
  });

  test("a keyword search city is reused by the thematic search", () => {
    storeLastKeywordSearchLocation({
      kind: LocationType.City,
      label: "Lyon (69)",
      searchParams: new URLSearchParams({ code_commune: "69123" }),
    });

    expect(getLastSearchLocation()).toEqual({
      cityCode: "69123",
      cityLabel: "Lyon (69)",
    });
  });

  test("a keyword search address is reused by the thematic search", () => {
    storeLastKeywordSearchLocation({
      kind: LocationType.Address,
      label: BORDEAUX_ADDRESS.label,
      cityLabel: "Bordeaux (33)",
      searchParams: new URLSearchParams({
        lon: "-0.57",
        lat: "44.83",
        code_insee: "33063",
      }),
    });

    expect(getLastSearchLocation()).toEqual(BORDEAUX_ADDRESS);
  });

  test.each([
    {
      kind: LocationType.Department,
      label: "Gironde (33)",
      searchParams: new URLSearchParams({ code_departement: "33" }),
    },
    {
      kind: LocationType.Region,
      label: "Nouvelle-Aquitaine",
      searchParams: new URLSearchParams({ code_region: "75" }),
    },
  ])(
    "a keyword search $label empties the thematic search location",
    (location) => {
      storeLastSearchLocation({ cityCode: "69123", cityLabel: "Lyon (69)" });
      storeLastKeywordSearchLocation(location);

      expect(loadLastLocation()?.label).toBe(location.label);
      expect(getLastSearchLocation()).toEqual({});
    }
  );

  test("clearing the keyword search location keeps the thematic one", () => {
    storeLastSearchLocation({ cityCode: "69123", cityLabel: "Lyon (69)" });
    storeLastKeywordSearchLocation(null);

    expect(loadLastLocation()).toBeNull();
    expect(getLastSearchLocation().cityLabel).toBe("Lyon (69)");
  });
});
