import type { Structure } from "#lib/types.js";
import { writable } from "svelte/store";

export const structure = writable<Structure>(undefined);
