import { error } from "@sveltejs/kit";
import type { OrientationExportType } from "$lib/requests/orientations";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async ({ parent, url }) => {
  await parent();

  const structureSlug = url.searchParams.get("structure");
  const type = url.searchParams.get("type");
  const token = url.searchParams.get("token");

  if (!structureSlug || !token || (type !== "sent" && type !== "received")) {
    error(404, "Page Not Found");
  }

  return {
    title: "Téléchargement des orientations | DORA",
    noIndex: true,
    structureSlug,
    type: type as OrientationExportType,
    token,
  };
};
