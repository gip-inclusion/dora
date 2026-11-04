import type { Structure } from "#lib/types.ts";
import { writable } from "svelte/store";

export const structure = writable<Structure>(undefined);
