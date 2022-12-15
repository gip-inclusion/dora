import type {
  DayPeriod,
  DayPrefix,
  OsmDay,
  OsmOpeningHours,
  OsmPeriodDay,
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
  const { timeSlot1, timeSlot2 } = lineday;

  if (!timeSlot1.isOpen && !timeSlot2.isOpen) return undefined;

  let str = `${prefix} `;

  if (timeSlot1.isOpen) str += `${timeSlot1.openAt}-${timeSlot1.closeAt}`;
  if (timeSlot1.isOpen && timeSlot2.isOpen) str += ",";
  if (timeSlot2.isOpen) str += `${timeSlot2.openAt}-${timeSlot2.closeAt}`;

  return str;
}

function isDayValid(lineday: OsmDay): boolean {
  return (
    isPeriodDayValid(lineday.timeSlot1) && isPeriodDayValid(lineday.timeSlot2)
  );
}
function isPeriodDayValid(period: OsmPeriodDay): boolean {
  if (!period.isOpen) return true;
  return !!period.closeAt && !!period.openAt;
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
    let dayKey: string;
    if (dayPrefix === "Mo") dayKey = "monday";
    if (dayPrefix === "Tu") dayKey = "tuesday";
    if (dayPrefix === "We") dayKey = "wednesday";
    if (dayPrefix === "Th") dayKey = "thursday";
    if (dayPrefix === "Fr") dayKey = "friday";
    if (dayPrefix === "Sa") dayKey = "saturday";
    if (dayPrefix === "Su") dayKey = "sunday";

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

export function returnEmptyHoursData(): OsmOpeningHours {
  return {
    monday: {
      timeSlot1: { isOpen: true, touched: false, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, touched: false, openAt: "", closeAt: "" },
    },
    tuesday: {
      timeSlot1: { isOpen: true, touched: false, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, touched: false, openAt: "", closeAt: "" },
    },
    wednesday: {
      timeSlot1: { isOpen: true, touched: false, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, touched: false, openAt: "", closeAt: "" },
    },
    thursday: {
      timeSlot1: { isOpen: true, touched: false, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, touched: false, openAt: "", closeAt: "" },
    },
    friday: {
      timeSlot1: { isOpen: true, touched: false, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, touched: false, openAt: "", closeAt: "" },
    },
    saturday: {
      timeSlot1: { isOpen: false, touched: false, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, touched: false, openAt: "", closeAt: "" },
    },
    sunday: {
      timeSlot1: { isOpen: false, touched: false, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, touched: false, openAt: "", closeAt: "" },
    },
  };
}

// On se base sur l'heure pour déterminer s'il s'agit d'une horaire d'après-midi ou non
// Note : une méthode plus fiable est-elle possible ?
function isAfternoonHour(hour: string): boolean {
  const hourStart = hour.substring(0, 2);
  return Number.parseInt(hourStart) > 12;
}

export function formatOsmHours(value: string) {
  let monday = "Fermé";
  let tuesday = "Fermé";
  let wednesday = "Fermé";
  let thursday = "Fermé";
  let friday = "Fermé";
  let saturday = undefined;
  let sunday = undefined;

  const hoursByDay = value.split(";");

  hoursByDay.forEach((hoursForDay) => {
    const [dayPrefix, hours] = hoursForDay.split(" ");

    if (dayPrefix === "Mo") monday = formatHour(hours);
    if (dayPrefix === "Tu") tuesday = formatHour(hours);
    if (dayPrefix === "We") wednesday = formatHour(hours);
    if (dayPrefix === "Th") thursday = formatHour(hours);
    if (dayPrefix === "Fr") friday = formatHour(hours);
    if (dayPrefix === "Sa") saturday = formatHour(hours);
    if (dayPrefix === "Su") sunday = formatHour(hours);
  });

  return [
    ["Lun.", monday],
    ["Mar.", tuesday],
    ["Mer.", wednesday],
    ["Jeu.", thursday],
    ["Ven.", friday],
    saturday && ["Sam.", saturday],
    sunday && ["Dim.", sunday],
  ].filter(Boolean);
}

// 09:00-12:00,14:00-18:30 => 09h00 - 12:00 / 14h00 - 18h30
function formatHour(hour: string) {
  hour = hour.replace(/-/g, " - ");
  hour = hour.replace(/:/g, "h");
  hour = hour.replace(/,/g, " / ");
  return hour;
}
