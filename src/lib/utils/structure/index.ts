import type {
  OsmOpeningHours,
  OsmDay,
  OsmPeriodDay,
  DayPrefix,
  DayPeriod,
} from "$lib/types";

export const INVALID_ERROR_MESSAGE = "Invalid";

export function fromJsonToOsmString(data: OsmOpeningHours) {
  if (
    isDayValid(data.monday) &&
    isDayValid(data.tuesday) &&
    isDayValid(data.wednesday) &&
    isDayValid(data.thursday) &&
    isDayValid(data.friday) &&
    isDayValid(data.saturday) &&
    isDayValid(data.sunday)
  ) {
    return [
      formatDay(data.monday, "Mo"),
      formatDay(data.tuesday, "Tu"),
      formatDay(data.wednesday, "We"),
      formatDay(data.thursday, "Th"),
      formatDay(data.friday, "Fr"),
      formatDay(data.saturday, "Sa"),
      formatDay(data.sunday, "Su"),
    ]
      .filter(Boolean)
      .join(";");
  }

  return INVALID_ERROR_MESSAGE;
}

function formatDay(lineday: OsmDay, prefix: DayPrefix): string | undefined {
  const { morning, afternoon } = lineday;

  if (!morning.isOpen && !afternoon.isOpen) return undefined;

  let str = `${prefix} `;

  if (morning.isOpen) str += `${morning.openAt}-${morning.closeAt}`;
  if (morning.isOpen && afternoon.isOpen) str += ",";
  if (afternoon.isOpen) str += `${afternoon.openAt}-${afternoon.closeAt}`;

  return str;
}

function isDayValid(lineday: OsmDay): boolean {
  return (
    isPeriodDayValid(lineday.morning) && isPeriodDayValid(lineday.afternoon)
  );
}
function isPeriodDayValid(period: OsmPeriodDay): boolean {
  if (!period.isOpen) return true;
  return !!period.closeAt && !!period.openAt;
}

export function getHoursFromStr(value: string): OsmOpeningHours {
  // Base object for all close
  const baseObject = returnEmptyHoursData();
  baseObject.monday.morning.isOpen = false;
  baseObject.monday.afternoon.isOpen = false;
  baseObject.tuesday.morning.isOpen = false;
  baseObject.tuesday.afternoon.isOpen = false;
  baseObject.wednesday.morning.isOpen = false;
  baseObject.wednesday.afternoon.isOpen = false;
  baseObject.thursday.morning.isOpen = false;
  baseObject.thursday.afternoon.isOpen = false;
  baseObject.friday.morning.isOpen = false;
  baseObject.friday.afternoon.isOpen = false;
  baseObject.saturday.morning.isOpen = false;
  baseObject.saturday.afternoon.isOpen = false;
  baseObject.sunday.morning.isOpen = false;
  baseObject.sunday.afternoon.isOpen = false;

  const hoursByDay = value.split(";");

  hoursByDay.forEach((hoursForDay) => {
    const [dayPrefix, hours] = hoursForDay.split(" ");

    // Jour concerné
    let dayKey: string;
    if (dayPrefix === "Mo") dayKey = "monday";
    if (dayPrefix === "Tu") dayKey = "tuesday";
    if (dayPrefix === "We") dayKey = "wednesday";
    if (dayPrefix === "Th") dayKey = "thursday";
    if (dayPrefix === "Fr") dayKey = "friday";
    if (dayPrefix === "Sa") dayKey = "saturday";
    if (dayPrefix === "Su") dayKey = "sunday";

    if (hours.includes(",")) {
      const [morningHours, afternoonHours] = hours.split(",");

      baseObject[dayKey].morning.isOpen = !!morningHours;
      baseObject[dayKey].afternoon.isOpen = !!afternoonHours;

      if (morningHours) {
        const [openAt, closeAt] = morningHours.split("-");
        baseObject[dayKey].morning.openAt = openAt;
        baseObject[dayKey].morning.closeAt = closeAt;
      }
      if (afternoonHours) {
        const [openAt, closeAt] = afternoonHours.split("-");
        baseObject[dayKey].afternoon.openAt = openAt;
        baseObject[dayKey].afternoon.closeAt = closeAt;
      }
    } else {
      // Horaire du matin ou de l'après-mdi
      const dayPeriodKey: DayPeriod = isAfternoonHour(hours)
        ? "afternoon"
        : "morning";

      const [openAt, closeAt] = hours.split("-");
      baseObject[dayKey][dayPeriodKey].isOpen = true;
      baseObject[dayKey][dayPeriodKey].openAt = openAt;
      baseObject[dayKey][dayPeriodKey].closeAt = closeAt;
    }
  });

  return baseObject;
}

export function returnEmptyHoursData(): OsmOpeningHours {
  return {
    monday: {
      morning: { isOpen: true, touched: false, openAt: "", closeAt: "" },
      afternoon: { isOpen: true, touched: false, openAt: "", closeAt: "" },
    },
    tuesday: {
      morning: { isOpen: true, touched: false, openAt: "", closeAt: "" },
      afternoon: { isOpen: true, touched: false, openAt: "", closeAt: "" },
    },
    wednesday: {
      morning: { isOpen: true, touched: false, openAt: "", closeAt: "" },
      afternoon: { isOpen: true, touched: false, openAt: "", closeAt: "" },
    },
    thursday: {
      morning: { isOpen: true, touched: false, openAt: "", closeAt: "" },
      afternoon: { isOpen: true, touched: false, openAt: "", closeAt: "" },
    },
    friday: {
      morning: { isOpen: true, touched: false, openAt: "", closeAt: "" },
      afternoon: { isOpen: true, touched: false, openAt: "", closeAt: "" },
    },
    saturday: {
      morning: { isOpen: false, touched: false, openAt: "", closeAt: "" },
      afternoon: { isOpen: false, touched: false, openAt: "", closeAt: "" },
    },
    sunday: {
      morning: { isOpen: false, touched: false, openAt: "", closeAt: "" },
      afternoon: { isOpen: false, touched: false, openAt: "", closeAt: "" },
    },
  };
}

// On se base sur l'heure pour déterminer s'il s'agit d'une horaire d'après-midi ou non
// Note : une méthode plus fiable est-elle possible ?
function isAfternoonHour(hour: string): boolean {
  const hourStart = hour.substring(0, 2);
  return Number.parseInt(hourStart) > 12;
}
