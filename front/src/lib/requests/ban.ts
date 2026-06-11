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
  const url = `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(term)}&limit=10`;
  const response = await fetch(url);
  if (response.ok) {
    const data = await response.json();
    return data.features;
  }
  return [];
}
