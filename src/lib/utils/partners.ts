import { shuffleArray } from "./array";

import logoAfpa from "$lib/assets/logos/partners/logo_afpa.png";
import logoAnlci from "$lib/assets/logos/partners/logo_anlci.png";
import logoApprentisAuteuils from "$lib/assets/logos/partners/logo_apprentisauteuils.png";
import logoBge from "$lib/assets/logos/partners/logo_bge.png";
import logoBonsClics from "$lib/assets/logos/partners/logo_bonsclics.png";
import logoBpi from "$lib/assets/logos/partners/logo_bpi.png";
import logoCheops from "$lib/assets/logos/partners/logo_cheops.png";
import logoCollectifEmploi from "$lib/assets/logos/partners/logo_collectifemploi.png";
import logoCravateSolidaire from "$lib/assets/logos/partners/logo_cravatesolidaire.png";
import logoCresus from "$lib/assets/logos/partners/logo_cresus.png";
import logoEc2 from "$lib/assets/logos/partners/logo_e2c.png";
import logoFace from "$lib/assets/logos/partners/logo_face.png";
import logoLesEmplois from "$lib/assets/logos/partners/logo_lesemplois.png";
import logoOrange from "$lib/assets/logos/partners/logo_orange.png";
import logoSocialBuilder from "$lib/assets/logos/partners/logo_socialbuilder.png";
import logoFinancesPedagogie from "$lib/assets/logos/partners/logo_financespedagogie.png";
import logoLigueEnseignement from "$lib/assets/logos/partners/logo_ligueenseignement.png";
import logoPositivePlanet from "$lib/assets/logos/partners/logo_posplanet.png";
import logoUniopss from "$lib/assets/logos/partners/logo_uniopss.png";
import logoForceFemmes from "$lib/assets/logos/partners/logo_forcefemmes.png";
import logoMedNum from "$lib/assets/logos/partners/logo_mednum.png";
import logoRenault from "$lib/assets/logos/partners/logo_renault.png";
import logoWiMoov from "$lib/assets/logos/partners/logo_wimoov.png";
import logoEpide from "$lib/assets/logos/partners/logo_epide.png";
import logoGoole from "$lib/assets/logos/partners/logo_google.png";
import logoMobin from "$lib/assets/logos/partners/logo_mobin.png";
import logoServiceCivique from "$lib/assets/logos/partners/logo_servicecivique.png";
import logoJeVeuxAider from "$lib/assets/logos/partners/logo_jeveuxaider.png";
import logoMonEnfant from "$lib/assets/logos/partners/logo_monenfantfr.png";
import logoSimplon from "$lib/assets/logos/partners/logo_simplon.png";
import logoKonexio from "$lib/assets/logos/partners/logo_konexio.png";
import logoNqt from "$lib/assets/logos/partners/logo_nqt.png";
import logoSNC from "$lib/assets/logos/partners/logo_snc.png";
import logoActionLogement from "$lib/assets/logos/partners/logo_actionlogement.png";
import logoArdennes from "$lib/assets/logos/partners/logo_ardennes.png";
import logoCAF from "$lib/assets/logos/partners/logo_caf.png";
import logoLaReunion from "$lib/assets/logos/partners/logo_lareunion.png";
import logoPoleEmploi from "$lib/assets/logos/partners/logo_poleemploi.png";

import type { Partner } from "$lib/types";

export const PARTNERS: Partner[] = [
  { name: "AFPA", img: logoAfpa },
  { name: "Crésus", img: logoCresus },
  { name: "Cheops", img: logoCheops },
  { name: "E2C", img: logoEc2 },
  { name: "BPI France", img: logoBpi },
  { name: "BGE", img: logoBge },
  {
    name: "La ligue de l’enseignement",
    img: logoLigueEnseignement,
  },
  { name: "Fondation FACE", img: logoFace },
  { name: "Positive Planet", img: logoPositivePlanet },
  { name: "SNC", img: logoSNC },
  { name: "Collectif Emploi", img: logoCollectifEmploi },
  { name: "NQT", img: logoNqt },
  { name: "Simplon.Co", img: logoSimplon },
  {
    name: "La cravate solidaire",
    img: logoCravateSolidaire,
  },
  { name: "Konexio", img: logoKonexio },
  { name: "Force Femmes", img: logoForceFemmes },
  {
    name: "Apprentis d’Auteuil",
    img: logoApprentisAuteuils,
  },
  { name: "La MedNum", img: logoMedNum },
  { name: "Renault", img: logoRenault },
  { name: "UNIOPSS", img: logoUniopss },
  { name: "Orange", img: logoOrange },
  { name: "ANLCI", img: logoAnlci },
  { name: "Les bons clics", img: logoBonsClics },
  { name: "Social Builder", img: logoSocialBuilder },
  { name: "Mobin", img: logoMobin },
  { name: "EPIDE", img: logoEpide },
  { name: "Wimoov", img: logoWiMoov },
  {
    name: "Les emplois de l’inclusion",
    img: logoLesEmplois,
  },
  { name: "JeVeuxAider", img: logoJeVeuxAider },
  { name: "Google - Ateliers numériques", img: logoGoole },
  { name: "Service Civique", img: logoServiceCivique },
  { name: "CNAF - Mon enfant.fr", img: logoMonEnfant },
  {
    name: "Finances et pédagogie (Caisse d’épargne)",
    img: logoFinancesPedagogie,
  },
  { name: "Action Logement", img: logoActionLogement },
  { name: "Conseil Départemental des Ardennes", img: logoArdennes },
  { name: "Caisse d‘allocations familiales", img: logoCAF },
  { name: "Département de la Réunion", img: logoLaReunion },
  { name: "Pôle emploi", img: logoPoleEmploi },
];

export function getPartners(limit?: number): Partner[] {
  return shuffleArray(PARTNERS).slice(0, limit || PARTNERS.length);
}
