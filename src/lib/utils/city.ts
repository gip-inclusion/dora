import type { ServicesOptions } from "$lib/types";

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
