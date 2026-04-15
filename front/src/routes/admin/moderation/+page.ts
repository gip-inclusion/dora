import type { PageLoad } from "./$types";
import { getStructuresToModerate } from "$lib/requests/admin";

export const load: PageLoad = ({ fetch }) => {
  return {
    structures: getStructuresToModerate(fetch).then((list) =>
      list.map((struct) => ({ ...struct, isStructure: true }))
    ),
    title: "Modération | Administration | DORA",
    noIndex: true,
  };
};
