import type { Structure } from "$lib/types";
import { writable } from "svelte/store";

export const structure = writable<Structure>(undefined);
