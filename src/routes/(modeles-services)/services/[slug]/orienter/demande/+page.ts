import { goto } from "$app/navigation";
import { get } from "svelte/store";
import { orientation } from "../store";

export const load = async ({ parent }) => {
  const data = await parent();

  if (!get(orientation).firstStepDone) {
    goto(`/services/${data.service.slug}/orienter`);
    return {};
  }

  return {
    ...data,
  };
};
