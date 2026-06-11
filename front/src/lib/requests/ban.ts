import { BAN_API_SEARCH_URL } from "$lib/consts";
import { getDepartmentFromCityCode } from "$lib/utils/misc";

interface BANProperties {
  label: string;
  id: string;
  postcode: string;
  city: string;
  district: string;
  street: string;
  housenumber: string;
  citycode: string;
  x: number;
  y: number;
  score: number;
  _score: number;
  name: string;
  type: string;
  _type: string;
  context: string;
  importance: number;
}
interface BANGeometry {
  type: string;
  coordinates: number[];
}
export interface BANFeature {
  type: string;
  properties: BANProperties;
  geometry: BANGeometry;
}

export async function search(term: string): Promise<BANFeature[]> {
  const url = `${BAN_API_SEARCH_URL}?q=${encodeURIComponent(term)}&limit=10`;
  const response = await fetch(url);
  const data = await response.json();
  if (response.ok) {
    return data.features;
  } else {
    if (data && data.detail.length) {
      // Le message est en anglais, mais on peut espérer le cas suffisamment
      // rare pour ne pas maintenir une traduction dans ce projet.
      throw new Error(data.detail[0]);
    }
    throw new Error(
      "Impossible d’effectuer une recherche d’adresse, veuillez réessayer."
    );
  }
}

export function formatMunicipality(feature: BANFeature) {
  return `${feature.properties.city} (${getDepartmentFromCityCode(
    feature.properties.citycode
  )})`;
}
