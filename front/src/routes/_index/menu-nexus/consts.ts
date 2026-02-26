import LogoLesEmplois from "$lib/assets/logos/logo-emploi-inclusion.svg";
import LogoDoraFull from "$lib/assets/logos/logo-dora-full.svg";
import LogoLeMarche from "$lib/assets/logos/logo-marche-inclusion.svg";
import LogoPilotage from "$lib/assets/logos/logo-pilotage-inclusion.svg";
import LogoMonRecap from "$lib/assets/logos/logo-monrecap.svg";

import type { NexusServiceID } from "$lib/requests/nexus";

export type NexusService = {
  id: NexusServiceID;
  icon: string;
  label: string;
  activated: {
    autologin: boolean;
    prodUrl: string;
    stagingUrl: string;
  };
  deactivated: {
    autologin: boolean;
    prodUrl: string;
    stagingUrl: string;
  };
};

export const ALL_SERVICES: NexusService[] = [
  {
    id: "les-emplois",
    label: "Les Emplois de l'inclusion",
    icon: LogoLesEmplois,
    activated: {
      autologin: true,
      prodUrl: "https://emplois.inclusion.beta.gouv.fr/dashboard/",
      stagingUrl: "https://demo.emplois.inclusion.beta.gouv.fr/dashboard/",
    },
    deactivated: {
      autologin: true,
      prodUrl: "https://emplois.inclusion.beta.gouv.fr/dashboard/",
      stagingUrl: "https://demo.emplois.inclusion.beta.gouv.fr/dashboard/",
    },
  },
  {
    id: "dora",
    label: "DORA",
    icon: LogoDoraFull,
    activated: {
      autologin: true,
      prodUrl: "https://dora.inclusion.gouv.fr/",
      stagingUrl: "https://staging.dora.inclusion.gouv.fr/",
    },
    deactivated: {
      autologin: true,
      prodUrl: "https://dora.inclusion.gouv.fr/",
      stagingUrl: "https://staging.dora.inclusion.gouv.fr/",
    },
  },
  {
    id: "le-marche",
    label: "Le Marché de l'inclusion",
    icon: LogoLeMarche,
    activated: {
      autologin: false,
      prodUrl: "https://lemarche.inclusion.gouv.fr/accounts/login",
      stagingUrl: "https://staging.lemarche.inclusion.gouv.fr/accounts/login",
    },
    deactivated: {
      autologin: false,
      prodUrl: "https://lemarche.inclusion.gouv.fr/accounts/signup",
      stagingUrl: "https://staging.lemarche.inclusion.gouv.fr/accounts/signup",
    },
  },
  {
    id: "pilotage",
    label: "Le Pilotage de l'inclusion",
    icon: LogoPilotage,
    activated: {
      autologin: true,
      prodUrl: "https://emplois.inclusion.beta.gouv.fr/dashboard/stats",
      stagingUrl: "https://demo.emplois.inclusion.beta.gouv.fr/dashboard/stats",
    },
    deactivated: {
      autologin: true,
      prodUrl: "https://emplois.inclusion.beta.gouv.fr/dashboard/stats",
      stagingUrl: "https://demo.emplois.inclusion.beta.gouv.fr/dashboard/stats",
    },
  },
  {
    id: "mon-recap",
    label: "Mon Récap",
    icon: LogoMonRecap,
    activated: {
      autologin: false,
      prodUrl:
        "https://mon-recap.inclusion.beta.gouv.fr/formulaire-commande-carnets",
      stagingUrl:
        "https://mon-recap.inclusion.beta.gouv.fr/formulaire-commande-carnets",
    },
    deactivated: {
      autologin: true,
      prodUrl:
        "https://emplois.inclusion.beta.gouv.fr/portal/service/mon-recap",
      stagingUrl:
        "https://demo.emplois.inclusion.beta.gouv.fr/portal/service/mon-recap",
    },
  },
];
