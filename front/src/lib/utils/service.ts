import BankLineBuildings from "svelte-remix/BankLineBuildings.svelte";
import ChatQuoteLineCommunication from "svelte-remix/ChatQuoteLineCommunication.svelte";
import ChatSmile3LineCommunication from "svelte-remix/ChatSmile3LineCommunication.svelte";
import CompassDiscoverLineMap from "svelte-remix/CompassDiscoverLineMap.svelte";
import MoneyEuroCircleLineFinance from "svelte-remix/MoneyEuroCircleLineFinance.svelte";
import GraduationCapLineOthers from "svelte-remix/GraduationCapLineOthers.svelte";
import HomeSmileLineBuildings from "svelte-remix/HomeSmileLineBuildings.svelte";
import MacLineDevice from "svelte-remix/MacLineDevice.svelte";
import MentalHealthLineHealthMedical from "svelte-remix/MentalHealthLineHealthMedical.svelte";
import ParentLineUserFaces from "svelte-remix/ParentLineUserFaces.svelte";
import WalkLineMap from "svelte-remix/WalkLineMap.svelte";
import Rocket2LineMap from "svelte-remix/Rocket2LineMap.svelte";
import ServiceLineBusiness from "svelte-remix/ServiceLineBusiness.svelte";
import StethoscopeLineHealthMedical from "svelte-remix/StethoscopeLineHealthMedical.svelte";
import Store2LineBuildings from "svelte-remix/Store2LineBuildings.svelte";
import TextEditor from "svelte-remix/TextEditor.svelte";
import WheelchairLineOthers from "svelte-remix/WheelchairLineOthers.svelte";

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
    return Rocket2LineMap;
  }
  if ("numerique" === slug) {
    return MacLineDevice;
  }
  if ("equipement-et-alimentation" === slug) {
    return Store2LineBuildings;
  }
  if ("famille" === slug) {
    return ParentLineUserFaces;
  }
  if ("gestion-financiere" === slug) {
    return MoneyEuroCircleLineFinance;
  }
  if ("apprendre-francais" === slug) {
    return ChatQuoteLineCommunication;
  }
  if ("accompagnement-social-et-professionnel-personnalise" === slug) {
    return ChatSmile3LineCommunication;
  }
  if ("handicap" === slug) {
    return WheelchairLineOthers;
  }
  if ("sante" === slug) {
    return StethoscopeLineHealthMedical;
  }
  if ("logement-hebergement" === slug) {
    return HomeSmileLineBuildings;
  }
  if ("illettrisme" === slug) {
    return TextEditor;
  }
  if ("mobilite" === slug) {
    return CompassDiscoverLineMap;
  }
  if ("remobilisation" === slug) {
    return MentalHealthLineHealthMedical;
  }
  if ("acces-aux-droits-et-citoyennete" === slug) {
    return BankLineBuildings;
  }
  if ("choisir-un-metier" === slug) {
    return ServiceLineBusiness;
  }
  if ("preparer-sa-candidature" === slug) {
    return ServiceLineBusiness;
  }
  if ("trouver-un-emploi" === slug) {
    return ServiceLineBusiness;
  }
  if ("se-former" === slug) {
    return GraduationCapLineOthers;
  }
  if ("souvrir-a-linternational" === slug) {
    return WalkLineMap;
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
