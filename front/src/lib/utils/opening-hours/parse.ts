import type { DayPeriod, DayPrefix, OsmDay, OsmOpeningHours } from "$lib/types";

import { INVALID_OPENING_HOURS_MARKER } from "./constants";

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

// On se base sur l'heure pour déterminer s'il s'agit d'une horaire d'après-midi ou non
// Note : une méthode plus fiable est-elle possible ?
function isAfternoonHour(hour: string): boolean {
  const hourStart = hour.substring(0, 2);
  return Number.parseInt(hourStart) > 12;
}

export function formatDay(lineday: OsmDay, prefix: DayPrefix): string | undefined {
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
