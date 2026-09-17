import type { DepartmentChoice } from "$lib/requests/geo";
import type { GeoApiValue } from "$lib/types";

const LAST_DEPARTMENT_STORAGE_KEY = "managerLastSelectedDepartment";

/**
 * Département à afficher sur les pages de gestion du territoire : le dernier
 * sélectionné s'il fait toujours partie des départements accessibles,
 * le premier sinon.
 */
export function getInitialDepartment(
  departments: DepartmentChoice[]
): GeoApiValue {
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

export function saveLastDepartment(department: GeoApiValue) {
  try {
    localStorage.setItem(LAST_DEPARTMENT_STORAGE_KEY, department.code);
  } catch {
    // Le localStorage peut être inaccessible.
  }
}
