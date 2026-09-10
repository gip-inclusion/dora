import DEPARTMENTS_DATA from "$lib/data/departments.json";
import REGIONS_DATA from "$lib/data/regions.json";

interface GeoSearchData {
  code: string;
  label: string;
  normalized: string;
}

interface GeoSearchCandidate {
  code: string;
  label: string;
  score: number;
}

interface GeoSearchResult {
  code: string;
  label: string;
}

function normalize(term: string) {
  return term
    .normalize("NFD")
    .replaceAll(/\p{Diacritic}/gu, "")
    .replaceAll(/[^\p{General_Category=Letter}]/gu, " ")
    .toLowerCase();
}

const DEPARTMENTS: GeoSearchData[] = Object.entries(DEPARTMENTS_DATA).map(
  ([code, name]) => ({
    code,
    label: name,
    normalized: normalize(name),
  })
);
const REGIONS: GeoSearchData[] = Object.entries(REGIONS_DATA).map(
  ([code, { name }]) => ({
    code,
    label: name,
    normalized: normalize(name),
  })
);

export function getRegionDepartments(code: string): string[] {
  return REGIONS_DATA[code as keyof typeof REGIONS_DATA]?.departments ?? [];
}

function bestMatch(
  data: GeoSearchData[],
  searchTerm: string
): GeoSearchResult | null {
  const normalizedSearchTerm = normalize(searchTerm);
  const matches = data
    .map(function ({ code, label, normalized }): GeoSearchCandidate | null {
      const score = normalized.indexOf(normalizedSearchTerm);
      if (score === -1) {
        return null;
      }
      return { code, label, score };
    })
    .filter((elt) => elt !== null)
    .sort((a, b) => a.score - b.score || a.label.localeCompare(b.label, "fr"));
  if (matches.length) {
    return { code: matches[0].code, label: matches[0].label };
  }
  return null;
}

export function searchDepartment(term: string): GeoSearchResult | null {
  return bestMatch(DEPARTMENTS, term);
}
export function searchRegion(term: string): GeoSearchResult | null {
  return bestMatch(REGIONS, term);
}

export function getDepartment(code: string): GeoSearchResult | null {
  const department = DEPARTMENTS.find((dept) => dept.code === code);
  return department ? { code: department.code, label: department.label } : null;
}
