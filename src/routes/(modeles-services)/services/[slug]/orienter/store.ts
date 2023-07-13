import { writable } from "svelte/store";
import type { Orientation } from "$lib/types";

export function initEmptyOrientation(): Orientation {
  return {
    /*
      // TODO: valeurs par defaut temporaires pour faciliter les tests du formulaire
      situation: ["Public femme en difficulté"],
      situationOther: "autre...",
      requirements: ["prerequis-1"],
      prescriberStructureSlug: "nenettes-co-le-resea",

      referentLastName: "RefName",
      referentFirstName: "RefFirstname",
      referentPhone: "1111111111",
      referentEmail: "ref@example.com",

      beneficiaryLastName: "BenName",
      beneficiaryFirstName: "BenFirstname",
      beneficiaryAvailability: "2023-07-04",
      beneficiaryContactPreferences: ["TELEPHONE", "AUTRE"],
      beneficiaryPhone: "2222222222",
      beneficiaryEmail: "ben@example.com",
      beneficiaryOtherContactMethod: "autre mode de contact",
      orientationReasons: "Motif de l’orientation",
    */
    firstStepDone: false,

    situation: [],
    situationOther: "",
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
