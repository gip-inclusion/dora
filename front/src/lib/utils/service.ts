import {
  bankIcon,
  chatQuoteIcon,
  chatSmileIcon,
  compassDiscoverIcon,
  euroLineIcon,
  graduationCapIcon,
  homeSmileIcon,
  macLineIcon,
  mentalHealthIcon,
  parentIcon,
  walkIcon,
  rocketIcon,
  serviceIcon,
  stethoscopeIcon,
  storeIcon,
  textIcon,
  wheelChairIcon,
} from "$lib/icons";
import type {
  Choice,
  FeeCondition,
  Model,
  Service,
  ServicesOptions,
  ServiceStatus,
} from "$lib/types";
import { isLessThanOneHourAgo } from "./date";
import { log } from "./logger";

export function getAvailableOptionsForStatus(
  status: ServiceStatus
): (ServiceStatus | "DELETE")[] {
  let result: (ServiceStatus | "DELETE")[] = [];

  if (status === "SUGGESTION") {
    result = ["DRAFT", "DELETE"];
  } else if (status === "PUBLISHED") {
    result = ["DRAFT", "ARCHIVED"];
  } else if (status === "DRAFT") {
    result = ["PUBLISHED", "ARCHIVED"];
  } else if (status === "ARCHIVED") {
    result = ["DRAFT"];
  } else {
    throw new Error(`Unknown status ${status}`);
  }

  return result;
}

export function getCategoryIcon(slug: string) {
  if ("creation-activite" === slug) {
    return rocketIcon;
  }
  if ("numerique" === slug) {
    return macLineIcon;
  }
  if ("equipement-et-alimentation" === slug) {
    return storeIcon;
  }
  if ("famille" === slug) {
    return parentIcon;
  }
  if ("gestion-financiere" === slug) {
    return euroLineIcon;
  }
  if ("apprendre-francais" === slug) {
    return chatQuoteIcon;
  }
  if ("accompagnement-social-et-professionnel-personnalise" === slug) {
    return chatSmileIcon;
  }
  if ("handicap" === slug) {
    return wheelChairIcon;
  }
  if ("sante" === slug) {
    return stethoscopeIcon;
  }
  if ("logement-hebergement" === slug) {
    return homeSmileIcon;
  }
  if ("illettrisme" === slug) {
    return textIcon;
  }
  if ("mobilite" === slug) {
    return compassDiscoverIcon;
  }
  if ("remobilisation" === slug) {
    return mentalHealthIcon;
  }
  if ("acces-aux-droits-et-citoyennete" === slug) {
    return bankIcon;
  }
  if ("choisir-un-metier" === slug) {
    return serviceIcon;
  }
  if ("preparer-sa-candidature" === slug) {
    return serviceIcon;
  }
  if ("trouver-un-emploi" === slug) {
    return serviceIcon;
  }
  if ("se-former" === slug) {
    return graduationCapIcon;
  }
  if ("souvrir-a-linternational" === slug) {
    return walkIcon;
  }
  log(`Pas d'icone définie pour la thématique ${slug}`);
  return null;
}

export function getCategoryLabel(
  slug: string,
  servicesOptions: ServicesOptions
) {
  const category = servicesOptions.categories.find((cat) => cat.value === slug);
  return category?.label ?? "";
}

export function getSubCategoryLabel(
  slug: string,
  servicesOptions: ServicesOptions
) {
  const subCategory = servicesOptions.subcategories.find(
    (subCat) => subCat.value === slug
  );
  return subCategory?.label ?? "";
}

export function isNotFreeService(feeConditionValue: FeeCondition): boolean {
  return feeConditionValue !== "gratuit";
}

export function associateIconToCategory(choices: Choice[]): Choice[] {
  choices.forEach((choice) => {
    choice.icon = getCategoryIcon(choice.value);
  });
  return choices;
}

export function sortCategory(categories: Choice[]) {
  return categories.sort((a, b) => {
    return a.label.localeCompare(b.label, "fr", { numeric: true });
  });
}

export function sortSubcategory(subcategories: Choice[]) {
  return subcategories.sort((a, b) => {
    if (a.value.endsWith("--autre")) {
      return 1;
    }
    if (b.value.endsWith("--autre")) {
      return -1;
    }

    if (a.value.endsWith("--all")) {
      return -1;
    }
    if (b.value.endsWith("--all")) {
      return 1;
    }

    return a.label.localeCompare(b.label, "fr", { numeric: true });
  });
}

export function sortByCategories(
  categories: Choice[],
  subcategories: Choice[]
) {
  const result: Choice[] = [];

  categories.forEach(({ value }) => {
    const subCategoriesForCategory = subcategories.filter((sub) =>
      sub.value.startsWith(value)
    );
    result.push(...sortSubcategory(subCategoriesForCategory));
  });
  return result;
}

export function isDurationValid(service: Service | Model): boolean {
  return (
    isFinite(service.durationWeeklyHours) &&
    service.durationWeeklyHours > 0 &&
    isFinite(service.durationWeeks) &&
    service.durationWeeks > 0
  );
}

export function isServiceRecentlyPublished(service: Service): boolean {
  return (
    !!service.publicationDate && isLessThanOneHourAgo(service.publicationDate)
  );
}
