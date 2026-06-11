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
    .replaceAll("-", " ")
    .replaceAll("'", " ")
    .normalize("NFD")
    .replaceAll(/\p{Diacritic}/gu, "")
    .toLowerCase();
}

const DEPARTMENTS: GeoSearchData[] = Object.entries(DEPARTMENTS_DATA).map(
  ([code, name]) => ({
    code: code,
    label: name,
    normalized: normalize(name),
  })
);
const REGIONS: GeoSearchData[] = Object.entries(REGIONS_DATA).map(
  ([code, name]) => ({
    code: code,
    label: name,
    normalized: normalize(name),
  })
);
function bestMatch(
  data: GeoSearchData[],
  searchTerm: string
): GeoSearchResult | null {
  const matches = data
    .map(function ({ code, label, normalized }): GeoSearchCandidate | null {
      const score = normalized.indexOf(normalize(searchTerm));
      if (score === -1) {
        return null;
      }
      return { code, label, score };
    })
    .filter((elt) => elt !== null)
    .sort(
      (
        { score: scoreA, label: labelA },
        { score: scoreB, label: labelB }
      ): number => {
        if (scoreA !== scoreB) {
          return scoreA - scoreB;
        } else {
          if (labelA < labelB) {
            return -1;
          } else if (labelB > labelA) {
            return 1;
          }
          return 0;
        }
      }
    );
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
