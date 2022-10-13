import {
  bankIcon,
  chatQuoteIcon,
  chatSmileIcon,
  compassDiscoverIcon,
  euroLineIcon,
  homeSmileIcon,
  macLineIcon,
  mentalHealthIcon,
  parentIcon,
  rocketIcon,
  serviceIcon,
  stethoscopeIcon,
  storeIcon,
  textIcon,
  wheelChairIcon,
} from "$lib/icons";
import {
  SERVICE_STATUSES,
  SERVICE_UPDATE_STATUS,
  type DashboardService,
  type FeeCondition,
  type Service,
  type ServicesOptions,
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
  if (service.status === SERVICE_STATUSES.PUBLISHED) {
    if (monthDiff >= 6 && monthDiff < 8)
      updateStatus = SERVICE_UPDATE_STATUS.NEEDED;
    if (monthDiff >= 8) updateStatus = SERVICE_UPDATE_STATUS.REQUIRED;
  }

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

export function getCategoryIcon(slug: string) {
  if ("creation-activite" === slug) return rocketIcon;
  if ("numerique" === slug) return macLineIcon;
  if ("equipement-alimentation" === slug) return storeIcon;
  if ("famille" === slug) return parentIcon;
  if ("difficultes-financieres" === slug) return euroLineIcon;
  if ("apprendre-francais" === slug) return chatQuoteIcon;
  if ("acc-global-indiv" === slug) return chatSmileIcon;
  if ("handicap" === slug) return wheelChairIcon;
  if ("sante" === slug) return stethoscopeIcon;
  if ("logement-hebergement" === slug) return homeSmileIcon;
  if ("illettrisme" === slug) return textIcon;
  if ("mobilite" === slug) return compassDiscoverIcon;
  if ("remobilisation" === slug) return mentalHealthIcon;
  if ("acces-aux-droits" === slug) return bankIcon;
  if ("emploi-choisir-metier" === slug) return serviceIcon;
  if ("emploi-preparer-sa-candidature" === slug) return serviceIcon;
  if ("emploi-trouver-emploi" === slug) return serviceIcon;
}

export function getCategoryLabel(
  slug: string,
  servicesOptions: ServicesOptions
) {
  const cat = servicesOptions.categories.find((s) => s.value === slug);
  return cat.label ?? "";
}

export function getSubCategoryLabel(
  slug: string,
  servicesOptions: ServicesOptions
) {
  const subCat = servicesOptions.subcategories.find((s) => s.value === slug);
  return subCat.label ?? "";
}

export function formatFilePath(filePath: string) {
  const file = filePath.split("/").pop();

  const dotPosition = file.lastIndexOf(".");
  if (dotPosition === -1) return file;

  const name = file.slice(0, dotPosition);
  const extension = file.slice(file.lastIndexOf("."), file.length);

  return `${name} (${extension})`;
}

export function isNotFreeService(feeConditionValue: FeeCondition): boolean {
  return feeConditionValue !== "gratuit";
}
