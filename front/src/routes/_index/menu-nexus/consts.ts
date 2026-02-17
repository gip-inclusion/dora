import LogoLesEmplois from "$lib/assets/logos/logo-emploi-inclusion.svg";
import LogoDoraFull from "$lib/assets/logos/logo-dora-full.svg";
import LogoLeMarche from "$lib/assets/logos/logo-marche-inclusion.svg";
import LogoPilotage from "$lib/assets/logos/logo-pilotage-inclusion.svg";
import LogoMonRecap from "$lib/assets/logos/logo-monrecap.svg";
import type { NexusServiceID } from "$lib/requests/nexus";

export type NexusService = {
  id: NexusServiceID;
  label: string;
  url: string;
  icon: string;
};

export const ALL_SERVICES: NexusService[] = [
  {
    id: "les-emplois",
    label: "Les Emplois de l’inclusion",
    url: "https://emplois.inclusion.beta.gouv.fr/dashboard/",
    icon: LogoLesEmplois,
  },
  {
    id: "dora",
    label: "DORA",
    url: "https://dora.inclusion.gouv.fr/structures/",
    icon: LogoDoraFull,
  },
  {
    id: "le-marche",
    label: "Le Marché de l’inclusion",
    url: "https://lemarche.inclusion.gouv.fr/profil/",
    icon: LogoLeMarche,
  },
  {
    id: "pilotage",
    label: "Le Pilotage de l’inclusion",
    url: "https://emplois.inclusion.beta.gouv.fr/dashboard/",
    icon: LogoPilotage,
  },
  {
    id: "mon-recap",
    label: "Mon Récap",
    url: "https://mon-recap.inclusion.beta.gouv.fr/formulaire-commande-carnets/",
    icon: LogoMonRecap,
  },
];
