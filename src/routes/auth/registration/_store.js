import { writable } from "svelte/store";
import { accountSchema } from "$lib/schemas/auth.js";

export const registrationInfo = writable(
  Object.fromEntries(
    Object.entries(accountSchema).map(([fieldName, props]) => [
      fieldName,
      props.default,
    ])
  )
);
