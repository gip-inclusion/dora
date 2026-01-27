import OpeningHours, { type optional_conf as OpeningConf } from "opening_hours";

import type { DayPeriod, DayPrefix, OsmDay, OsmOpeningHours } from "$lib/types";

export const INVALID_OPENING_HOURS_MARKER = "##INVALID##";

function formatDay(lineday: OsmDay, prefix: DayPrefix): string | undefined {
  const { timeSlot1, timeSlot2 } = lineday;

  const timeSlot1HasValues: boolean = !!timeSlot1.openAt || !!timeSlot1.closeAt;
  const timeSlot2HasValues: boolean = !!timeSlot2.openAt || !!timeSlot2.closeAt;

  // Les jours mais sans valeurs sont ignorés - même s'ils sont ouverts dans le formulaire
  if (!timeSlot1HasValues && !timeSlot2HasValues) {
    return undefined;
  }

  const timeSlot1Valid: boolean =
    !!timeSlot1.openAt &&
    !!timeSlot1.closeAt &&
    timeSlot1.openAt < timeSlot1.closeAt;

  const timeSlot2Valid: boolean =
    !!timeSlot2.openAt &&
    !!timeSlot2.closeAt &&
    timeSlot2.openAt < timeSlot2.closeAt;

  let str = `${prefix} `;
  if (timeSlot1.isOpen && timeSlot1HasValues) {
    if (timeSlot1Valid) {
      str += `${timeSlot1.openAt}-${timeSlot1.closeAt}`;
    } else {
      str += INVALID_OPENING_HOURS_MARKER;
    }
  }

  if (
    timeSlot1.isOpen &&
    timeSlot1HasValues &&
    timeSlot2.isOpen &&
    timeSlot2HasValues
  ) {
    str += ",";
  }

  if (timeSlot2.isOpen && timeSlot2HasValues) {
    if (timeSlot2Valid) {
      str += `${timeSlot2.openAt}-${timeSlot2.closeAt}`;
    } else {
      str += INVALID_OPENING_HOURS_MARKER;
    }
  }

  return str;
}

// On se base sur l'heure pour déterminer s'il s'agit d'une horaire d'après-midi ou non
// Note : une méthode plus fiable est-elle possible ?
function isAfternoonHour(hour: string): boolean {
  const hourStart = hour.substring(0, 2);
  return Number.parseInt(hourStart) > 12;
}

export function returnEmptyHoursData(): OsmOpeningHours {
  return {
    monday: {
      timeSlot1: { isOpen: true, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    },
    tuesday: {
      timeSlot1: { isOpen: true, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    },
    wednesday: {
      timeSlot1: { isOpen: true, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    },
    thursday: {
      timeSlot1: { isOpen: true, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    },
    friday: {
      timeSlot1: { isOpen: true, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    },
    saturday: {
      timeSlot1: { isOpen: false, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    },
    sunday: {
      timeSlot1: { isOpen: false, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    },
  };
}

export function getHoursFromStr(value: string): OsmOpeningHours {
  // Base object for all close
  const baseObject = returnEmptyHoursData();
  baseObject.monday.timeSlot1.isOpen = false;
  baseObject.monday.timeSlot2.isOpen = false;
  baseObject.tuesday.timeSlot1.isOpen = false;
  baseObject.tuesday.timeSlot2.isOpen = false;
  baseObject.wednesday.timeSlot1.isOpen = false;
  baseObject.wednesday.timeSlot2.isOpen = false;
  baseObject.thursday.timeSlot1.isOpen = false;
  baseObject.thursday.timeSlot2.isOpen = false;
  baseObject.friday.timeSlot1.isOpen = false;
  baseObject.friday.timeSlot2.isOpen = false;
  baseObject.saturday.timeSlot1.isOpen = false;
  baseObject.saturday.timeSlot2.isOpen = false;
  baseObject.sunday.timeSlot1.isOpen = false;
  baseObject.sunday.timeSlot2.isOpen = false;

  const hoursByDay = value.split(";");

  hoursByDay.forEach((hoursForDay) => {
    const [dayPrefix, hours] = hoursForDay.split(" ");

    // Jour concerné
    let dayKey = "";
    if (dayPrefix === "Mo") {
      dayKey = "monday";
    }
    if (dayPrefix === "Tu") {
      dayKey = "tuesday";
    }
    if (dayPrefix === "We") {
      dayKey = "wednesday";
    }
    if (dayPrefix === "Th") {
      dayKey = "thursday";
    }
    if (dayPrefix === "Fr") {
      dayKey = "friday";
    }
    if (dayPrefix === "Sa") {
      dayKey = "saturday";
    }
    if (dayPrefix === "Su") {
      dayKey = "sunday";
    }

    if (hours.includes(",")) {
      const [timeSlot1Hours, timeSlot2Hours] = hours.split(",");

      baseObject[dayKey].timeSlot1.isOpen = !!timeSlot1Hours;
      baseObject[dayKey].timeSlot2.isOpen = !!timeSlot2Hours;

      if (timeSlot1Hours) {
        const [openAt, closeAt] = timeSlot1Hours.split("-");
        baseObject[dayKey].timeSlot1.openAt = openAt;
        baseObject[dayKey].timeSlot1.closeAt = closeAt;
      }
      if (timeSlot2Hours) {
        const [openAt, closeAt] = timeSlot2Hours.split("-");
        baseObject[dayKey].timeSlot2.openAt = openAt;
        baseObject[dayKey].timeSlot2.closeAt = closeAt;
      }
    } else {
      // Horaire du matin/journée ou de l'après-mdi
      const dayPeriodKey: DayPeriod = isAfternoonHour(hours)
        ? "timeSlot2"
        : "timeSlot1";

      const [openAt, closeAt] = hours.split("-");
      baseObject[dayKey][dayPeriodKey].isOpen = true;
      baseObject[dayKey][dayPeriodKey].openAt = openAt;
      baseObject[dayKey][dayPeriodKey].closeAt = closeAt;
    }
  });

  return baseObject;
}

// 09:00-12:00,14:00-18:30 => 09h00 - 12:00 / 14h00 - 18h30
function formatHour(hour: string) {
  hour = hour.replace(/-/g, " - ");
  hour = hour.replace(/:/g, "h");
  hour = hour.replace(/,/g, " / ");
  return hour;
}

// Convertit l'index de jour JavaScript (0=dimanche) vers notre format (0=lundi)
function toDayIndex(jsDayIndex: number): number {
  return jsDayIndex === 0 ? 6 : jsDayIndex - 1;
}

// Formate les horaires d'un jour
function formatDayHours(
  dayIntervals: Array<[Date, Date]>,
  timeFormatter: Intl.DateTimeFormat
): string {
  if (dayIntervals.length === 0) {
    return "Fermé";
  }

  // Trie les intervalles par heure de début
  const sortedIntervals = [...dayIntervals].sort(
    (a, b) => a[0].getTime() - b[0].getTime()
  );

  // Formate chaque intervalle en "HH:mm-HH:mm"
  const timeRanges = sortedIntervals.map(([start, end]) => {
    const startTime = timeFormatter.format(start);
    const endTime = timeFormatter.format(end);
    return `${startTime}-${endTime}`;
  });

  // Applique le formatage français (":" -> "h", "," -> " / ")
  return formatHour(timeRanges.join(","));
}

// Obtient le nom localisé d'un jour (ex: "Lun.")
function getDayName(
  dayIndex: number,
  weekStart: Date,
  dayFormatter: Intl.DateTimeFormat
): string {
  const dayDate = new Date(weekStart);
  dayDate.setDate(weekStart.getDate() + dayIndex);
  const dayName = dayFormatter.format(dayDate);
  return dayName.charAt(0).toUpperCase() + dayName.slice(1);
}

export function formatOsmHours(value: string): Array<[string, string]> | null {
  try {
    const openingHoursInstance = new OpeningHours(value, null, {
      locale: "fr",
    } as OpeningConf);

    const timeFormatter = new Intl.DateTimeFormat("fr-FR", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });

    const dayFormatter = new Intl.DateTimeFormat("fr-FR", {
      weekday: "short",
    });

    // Calcule le lundi de la semaine courante comme référence
    const now = new Date();
    const currentDay = now.getDay(); // 0 = dimanche, 1 = lundi, etc.
    const daysFromMonday = currentDay === 0 ? 6 : currentDay - 1;
    const weekStart = new Date(now);
    weekStart.setDate(now.getDate() - daysFromMonday);
    weekStart.setHours(0, 0, 0, 0);

    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 7);

    // Récupère tous les intervalles ouverts de la semaine
    const intervals = openingHoursInstance.getOpenIntervals(weekStart, weekEnd);

    // Groupe les intervalles par jour de la semaine (0 = lundi, 6 = dimanche)
    const intervalsByDay: Array<Array<[Date, Date]>> = Array.from(
      { length: 7 },
      () => []
    );

    intervals.forEach(([start, end]) => {
      const dayIndex = toDayIndex(start.getDay());
      intervalsByDay[dayIndex].push([start, end]);
    });

    // Formate tous les jours de la semaine
    const formattedDays = intervalsByDay.map((dayIntervals, dayIndex) => {
      const hours = formatDayHours(dayIntervals, timeFormatter);
      const isWeekday = dayIndex < 5; // 0-4 = lundi à vendredi

      // Toujours afficher les jours de semaine, même s'ils sont fermés
      if (isWeekday) {
        return [getDayName(dayIndex, weekStart, dayFormatter), hours];
      }

      // Pour samedi-dimanche, n'afficher que s'ils ne sont pas fermés
      return hours !== "Fermé"
        ? [getDayName(dayIndex, weekStart, dayFormatter), hours]
        : null;
    });

    // Filtre uniquement les jours weekend fermés (null) et retourne le résultat
    return formattedDays.filter((day): day is [string, string] => day !== null);
  } catch {
    // En cas d'erreur de parsing, retourne null pour indiquer un format invalide
    return null;
  }
}

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
