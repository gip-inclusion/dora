import { error } from "@sveltejs/kit";

export const load = async ({ parent }) => {
  const data = await parent();
  const { service } = data;

  // on ne doit pas pouvoir accèder à cette page
  // si le service n'est pas orientable
  if (!service.isOrientable) {
    error(400, "Service non-orientable");
  }

  return {
    ...data,
  };
};
