import type { OsmOpeningHours } from "$lib/types";

import { formatDay } from "./parse";

export function fromJsonToOsmString(data: OsmOpeningHours) {
  let days: string[] = [];

  days.push(formatDay(data.monday, "Mo") || "");
  days.push(formatDay(data.tuesday, "Tu") || "");
  days.push(formatDay(data.wednesday, "We") || "");
  days.push(formatDay(data.thursday, "Th") || "");
  days.push(formatDay(data.friday, "Fr") || "");
  days.push(formatDay(data.saturday, "Sa") || "");
  days.push(formatDay(data.sunday, "Su") || "");

  days = days.filter(Boolean);
  if (days.length) {
    return days.join(";");
  }

  // TODO: vérifier le meilleur moyen de propager l'erreur
  return null;
}
