import BankLineBuildings from "svelte-remix/BankLineBuildings.svelte";
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
  if (status === "SUGGESTION") {
    return ["DRAFT", "DELETE"];
  } else if (status === "PUBLISHED") {
    return ["DRAFT", "ARCHIVED"];
  } else if (status === "DRAFT") {
    return ["PUBLISHED", "ARCHIVED"];
  } else if (status === "ARCHIVED") {
    return ["DRAFT"];
  }

  throw new Error(`Unknown status ${status}`);
}
const CATEGORY_ICONS = {
  "choisir-un-metier": ServiceLineBusiness,
  "creer-une-entreprise": Rocket2LineMap,
  "difficultes-administratives-ou-juridiques": BankLineBuildings,
  "difficultes-financieres": MoneyEuroCircleLineFinance,
  "equipement-et-alimentation": Store2LineBuildings,
  famille: ParentLineUserFaces,
  "lecture-ecriture-calcul": TextEditor,
  "logement-hebergement": HomeSmileLineBuildings,
  mobilite: CompassDiscoverLineMap,
  numerique: MacLineDevice,
  "preparer-sa-candidature": ServiceLineBusiness,
  remobilisation: MentalHealthLineHealthMedical,
  sante: StethoscopeLineHealthMedical,
  "se-former": GraduationCapLineOthers,
  "souvrir-a-linternational": WalkLineMap,
  "trouver-un-emploi": ServiceLineBusiness,
};

export function getCategoryIcon(slug: string) {
  if (CATEGORY_ICONS[slug]) {
    return CATEGORY_ICONS[slug];
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
