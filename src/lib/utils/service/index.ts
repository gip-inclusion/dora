import {
  SERVICE_STATUSES,
  SERVICE_UPDATE_STATUS,
  type DashboardService,
  type Service,
} from "$lib/types";
import dayjs from "dayjs";

export function getAvailableOptionsForStatus(
  status: SERVICE_STATUSES
): (SERVICE_STATUSES | "DELETE")[] {
  let result: (SERVICE_STATUSES | "DELETE")[] = [];

  if (status === SERVICE_STATUSES.SUGGESTION) {
    result = [SERVICE_STATUSES.DRAFT, "DELETE"];
  } else if (status === SERVICE_STATUSES.PUBLISHED) {
    result = [SERVICE_STATUSES.DRAFT, SERVICE_STATUSES.ARCHIVED];
  } else if (status === SERVICE_STATUSES.DRAFT) {
    result = [SERVICE_STATUSES.PUBLISHED, SERVICE_STATUSES.ARCHIVED];
  } else if (status === SERVICE_STATUSES.ARCHIVED) {
    result = [SERVICE_STATUSES.DRAFT];
  } else {
    throw new Error(`Unknown status ${status}`);
  }

  return result;
}

type ServiceUpdateStatusData = {
  dayDiff: number;
  weekDiff: number;
  monthDiff: number;
  yearDiff: number;
  updateStatus: SERVICE_UPDATE_STATUS;
};
export function computeUpdateStatusData(
  service: Service | DashboardService
): ServiceUpdateStatusData {
  const lastUpdateDay = dayjs(service.modificationDate);
  const dayDiff = dayjs().diff(lastUpdateDay, "day");
  const weekDiff = dayjs().diff(lastUpdateDay, "week");
  const monthDiff = dayjs().diff(lastUpdateDay, "month");
  const yearDiff = dayjs().diff(lastUpdateDay, "year");

  let updateStatus = SERVICE_UPDATE_STATUS.NOT_NEEDED;
  if (monthDiff >= 6 && monthDiff < 8)
    updateStatus = SERVICE_UPDATE_STATUS.NEEDED;
  if (monthDiff >= 8) updateStatus = SERVICE_UPDATE_STATUS.REQUIRED;

  return {
    dayDiff,
    weekDiff,
    monthDiff,
    yearDiff,
    updateStatus,
  };
}

export function computeUpdateStatusLabel({
  dayDiff,
  weekDiff,
  monthDiff,
  yearDiff,
}: {
  dayDiff: number;
  weekDiff: number;
  monthDiff: number;
  yearDiff: number;
}) {
  let label = "";
  if (dayDiff < 1) {
    label = "Actualisé aujourd'hui";
  } else if (dayDiff < 7) {
    label = `Actualisé il y a ${dayDiff} jour${dayDiff > 1 ? "s" : ""}`;
  } else if (weekDiff <= 5) {
    label = `Actualisé il y a ${weekDiff} semaine${weekDiff > 1 ? "s" : ""}`;
  } else if (monthDiff < 12) {
    label = `Actualisé il y a ${monthDiff} mois`;
  } else {
    label = `Actualisé il y a plus de ${yearDiff} an${yearDiff > 1 ? "s" : ""}`;
  }
  return label;
}
