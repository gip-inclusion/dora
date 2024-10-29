import { browser } from "$app/environment";
import type { ServicesOptions } from "$lib/types";
import { defaultAcceptHeader } from "$lib/utils/api";
import { token } from "$lib/utils/auth";
import insane from "insane";
import showdown from "showdown";
import { get } from "svelte/store";

const { defaults } = insane;

const INSANE_CONFIGURATION = {
  ...defaults,
  allowedAttributes: {
    ...defaults.allowedAttributes,
    a: [...defaults.allowedAttributes.a, "rel", "class"],
  },
};

export function markdownToHTML(
  markdownContent: string,
  titleLevel: number | undefined = undefined
) {
  const converter = new showdown.Converter({
    headerLevelStart: titleLevel,
    tables: true,
    openLinksInNewWindow: true,
    simplifiedAutoLink: true,
  });

  return insane(converter.makeHtml(markdownContent), INSANE_CONFIGURATION);
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
  const currentToken = get(token);

  if (currentToken) {
    headers.Authorization = `Token ${currentToken}`;
  }

  const response = await fetch(url, {
    headers,
  });

  return {
    ok: response.ok,
    data: response.ok ? ((await response.json()) as T) : null,
    error: response.ok ? null : response.statusText,
    status: response.status,
    statusText: response.statusText,
  };
}

export function shortenString(str, length = 50) {
  if (str && str.length > length) {
    return `${str.slice(0, length - 1)}…`;
  }

  return str;
}

export function capitalize(text: string) {
  if (text.toUpperCase() !== text) {
    // Si le texte n'est pas en capitales
    // on considère qu'il a été édité par l'utilisateur et on l'affiche tel quel
    return text;
  }
  // Sinon on essaye de faire le moins de dégats possible dans la capitalisation…
  let result = text
    .toLowerCase()
    .replace(/^\w|[\s\-'’]\w/gu, (char: string) => char.toUpperCase());

  const stopWords = [
    "De",
    "Des",
    "Du",
    "Et",
    "À",
    "A",
    "Au",
    "En",
    "La",
    "Le",
    "Les",
    "L",
    "D",
    "Sur",
    "Pour",
  ];
  for (const stopWord of stopWords) {
    const regex = new RegExp(`([\\s\\-'’])${stopWord}([\\s\\-'’])`, "g");
    result = result.replace(regex, `$1${stopWord.toLowerCase()}$2`);
  }

  return result;
}

export function getDepartmentFromCityCode(cityCode) {
  if (cityCode == null) {
    return null;
  }

  return cityCode.startsWith("97")
    ? cityCode.slice(0, 3)
    : cityCode.slice(0, 2);
}

export function moveToTheEnd(
  array,
  key,
  value,
  { sortBeginning = false, sortKey = "label" } = {}
) {
  const elementsToMove = array.filter((elt) => elt[key] === value);

  if (!elementsToMove.length) {
    return array;
  }

  let beginning = array.filter((elt) => elt[key] !== value);
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
  const selectedCategories = servicesOptions.categories.filter((option) =>
    categoriesValues.includes(option.value)
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
  if (a === b) {
    return true;
  }
  if (a == null || b == null) {
    return false;
  }
  if (a.length !== b.length) {
    return false;
  }

  return a.every((val, i) => val === b[i]);
}

export function formatPhoneNumber(phoneNumber: string): string {
  let result = "";
  phoneNumber.split("").forEach((char, i) => {
    if (i !== 0 && i % 2 === 0) {
      result += " ";
    }
    result += char;
  });
  return result;
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

export function clickOutside(node: HTMLElement) {
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore erreurs de typage inextricables...
  const handleClick = (event) => {
    if (node && !node.contains(event.target) && !event.defaultPrevented) {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore erreurs de typage inextricables...
      node.dispatchEvent(new CustomEvent("click_outside", node));
    }
  };

  document.addEventListener("click", handleClick, true);

  return {
    destroy() {
      document.removeEventListener("click", handleClick, true);
    },
  };
}

// Helper type pour aplatir les promesses
type Awaited<T> = T extends PromiseLike<infer U> ? U : T;

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  delay = 300
): (...args: Parameters<T>) => Promise<Awaited<ReturnType<T>>> {
  let timeoutId: ReturnType<typeof setTimeout>;

  return (...args: Parameters<T>) => {
    return new Promise<Awaited<ReturnType<T>>>((resolve) => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      } // Réinitialiser le timeout s'il existe déjà
      timeoutId = setTimeout(() => {
        const result = func(...args);
        resolve(result); // Résout avec le résultat, qui peut être une promesse ou une valeur simple
      }, delay);
    });
  };
}
