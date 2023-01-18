import { browser } from "$app/environment";
import type { ServicesOptions } from "$lib/types";
import { defaultAcceptHeader } from "$lib/utils/api";
import { token } from "$lib/utils/auth";
import insane from "insane";
import showdown from "showdown";
import { get } from "svelte/store";

export function markdownToHTML(md, titleLevel) {
  const converter = new showdown.Converter({
    headerLevelStart: titleLevel ?? 2,
    tables: true,
    openLinksInNewWindow: true,
    simplifiedAutoLink: true,
  });

  return insane(converter.makeHtml(md));
}

export function htmlToMarkdown(html: string) {
  if (browser) {
    const converter = new showdown.Converter();
    return converter.makeMarkdown(html);
  }

  return "";
}

export async function fetchData<T>(url: string) {
  const headers = { Accept: defaultAcceptHeader };
  const tk = get(token);

  if (tk) {
    headers["Authorization"] = `Token ${tk}`;
  }

  const response = await fetch(url, {
    headers,
  });

  return {
    ok: response.ok,
    data: response.ok ? ((await response.json()) as Promise<T>) : null,
    error: response.ok ? null : response.statusText,
    status: response.status,
    statusText: response.statusText,
  };
}

export function shortenString(str, length = 50) {
  if (str && str.length > length) {
    return `${str.slice(0, length)}…`;
  }

  return str;
}

export function capitalize(str) {
  return str.toLowerCase().replace(/^\w|\s\w/gu, (c) => c.toUpperCase());
}

export function getDepartmentFromCityCode(cityCode) {
  if (cityCode == null) {
    return null;
  }

  return cityCode.startsWith("97")
    ? cityCode.slice(0, 3)
    : cityCode.slice(0, 2);
}

export function addlinkToUrls(text) {
  const urlRegex = /((https?|mailto):\/\/[^\s]+\.[^\s]+)/gu;

  return insane(
    text.replace(
      urlRegex,
      (url) =>
        `<a href="${url}" class="underline" rel="noopener nofollow">${url}</a>`
    ),
    { allowedTags: ["a"], allowedAttributes: { a: ["class", "rel", "href"] } }
  );
}

export function moveToTheEnd(
  array,
  key,
  value,
  { sortBeginning = false, sortKey = "label" } = {}
) {
  const elementsToMove = array.filter((e) => e[key] === value);

  if (!elementsToMove.length) {
    return array;
  }

  let beginning = array.filter((e) => e[key] !== value);
  if (sortBeginning) {
    beginning = beginning.sort((a, b) =>
      a[sortKey].localeCompare(b[sortKey], "fr", { numeric: true })
    );
  }

  return [...beginning, ...elementsToMove];
}

export function orderAndReformatSubcategories(
  subcategoriesValues,
  categoriesValues,
  servicesOptions
) {
  const selectedCategories = servicesOptions.categories.filter((so) =>
    categoriesValues.includes(so.value)
  );

  return moveToTheEnd(subcategoriesValues, "label", "Autre", {
    sortBeginning: true,
    sortKey: "value",
  }).map(({ value, label }) => {
    const categorie = selectedCategories.find(
      (cat) => cat.value === value.split("--")[0]
    );
    return {
      value,
      label:
        selectedCategories.length > 1
          ? `${label} (${categorie?.label})`
          : label,
    };
  });
}

export function arraysCompare(a, b) {
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (a.length !== b.length) return false;

  return a.every((val, i) => val === b[i]);
}

export function formatPhoneNumber(phoneNumber: string): string {
  try {
    return phoneNumber.match(/.{2}/g).join(" ");
  } catch {
    // On ne cherche pas à logguer l'erreur ici, ce sera fait
    // dans les scripts de nettoyage de la BDD
    return phoneNumber;
  }
}

export function isInDeploymentDepartments(
  cityCode: string,
  servicesOptions: ServicesOptions
): boolean {
  return (
    (servicesOptions.deploymentDepartments || []).filter((department) =>
      cityCode.startsWith(department)
    ).length > 0
  );
}
