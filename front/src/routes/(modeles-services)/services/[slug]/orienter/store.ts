import { writable } from "svelte/store";
import type { Orientation } from "$lib/types";

export function initEmptyOrientation(): Orientation {
  return {
    firstStepDone: false,
    contactBoxOpen: false,

    situation: [],
    requirements: [],
    prescriberStructureSlug: "",

    referentLastName: "",
    referentFirstName: "",
    referentPhone: "",
    referentEmail: "",

    beneficiaryLastName: "",
    beneficiaryFirstName: "",
    beneficiaryAvailability: new Date().toISOString().split("T")[0],
    beneficiaryContactPreferences: [],
    beneficiaryPhone: "",
    beneficiaryEmail: "",
    beneficiaryOtherContactMethod: "",
    orientationReasons: "",

    attachments: {},
  };
}

export const orientation = writable<Orientation>(initEmptyOrientation());
