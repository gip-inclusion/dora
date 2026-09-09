import { getDepartments, type DepartmentChoice } from "$lib/requests/geo";
import type { GeoApiValue } from "$lib/types";
import { userInfo } from "$lib/utils/auth";
import { error } from "@sveltejs/kit";
import { get } from "svelte/store";

const LAST_DEPARTMENT_STORAGE_KEY = "managerLastSelectedDepartment";

/**
 * Département à afficher sur les pages de gestion du territoire : le dernier
 * sélectionné s'il fait toujours partie des départements accessibles
 * à l'utilisateur, le premier sinon.
 */
function getInitialDepartment(departments: DepartmentChoice[]): GeoApiValue {
  let lastCode: string | null = null;
  try {
    lastCode = localStorage.getItem(LAST_DEPARTMENT_STORAGE_KEY);
  } catch {
    // Le localStorage peut être inaccessible.
  }

  return (
    departments.find((department) => department.value.code === lastCode)
      ?.value ?? departments[0].value
  );
}

/**
 * Départements accessibles à l'utilisateur et département à sélectionner par
 * défaut, pour les pages de gestion du territoire.
 */
export async function loadManagerDepartments(fetchFunction = fetch): Promise<{
  departments: DepartmentChoice[];
  department: GeoApiValue;
}> {
  const user = get(userInfo);

  const departments = await getDepartments(
    // Le staff a normalement accès à tous les départements.
    user?.isStaff ? [] : (user?.departments ?? []),
    fetchFunction
  );

  // Si la requête échoue, ce n'est pas un problème de droits.
  if (!departments) {
    error(500, "Impossible de récupérer la liste des départements");
  }

  if (!departments.length) {
    error(403, "Accès réservé");
  }

  return { departments, department: getInitialDepartment(departments) };
}

export function saveLastDepartment(department: GeoApiValue) {
  try {
    localStorage.setItem(LAST_DEPARTMENT_STORAGE_KEY, department.code);
  } catch {
    // Le localStorage peut être inaccessible.
  }
}
