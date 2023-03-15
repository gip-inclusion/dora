<script lang="ts">
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

  export const PARTNERS: Record<string, Partner> = {
    // "Action logement",
    afpa: { name: "AFPA", img: logoAfpa },
    cresus: { name: "Crésus", img: logoCresus },
    cheops: { name: "Cheops", img: logoCheops },
    e2c: { name: "E2C", img: logoEc2 },
    bpi: { name: "BPI France", img: logoBpi },
    bge: { name: "BGE", img: logoBge },
    ligueEnseignement: {
      name: "La ligue de l’enseignement",
      img: logoLigueEnseignement,
    },
    fondationFace: { name: "Fondation FACE", img: logoFace },
    positivePlanet: { name: "Positive Planet", img: logoPositivePlanet },
    snc: { name: "SNC", img: logoSNC },
    collectifEmploi: { name: "Collectif Emploi", img: logoCollectifEmploi },
    nqt: { name: "NQT", img: logoNqt },
    simplon: { name: "Simplon.Co", img: logoSimplon },
    cravateSolidaire: {
      name: "La cravate solidaire",
      img: logoCravateSolidaire,
    },
    konexio: { name: "Konexio", img: logoKonexio },
    forceFemmes: { name: "Force Femmes", img: logoForceFemmes },
    apprentisAuteuils: {
      name: "Apprentis d’Auteuil",
      img: logoApprentisAuteuils,
    },
    medNum: { name: "La MedNum", img: logoMedNum },
    renault: { name: "Renault", img: logoRenault },
    uniopss: { name: "UNIOPSS", img: logoUniopss },
    orange: { name: "Orange", img: logoOrange },
    anlci: { name: "ANLCI", img: logoAnlci },
    bonsClics: { name: "Les bons clics", img: logoBonsClics },
    socialBuilder: { name: "Social Builder", img: logoSocialBuilder },
    mobin: { name: "Mobin", img: logoMobin },
    epide: { name: "EPIDE", img: logoEpide },
    wimoov: { name: "Wimoov", img: logoWiMoov },
    emploisInclusion: {
      name: "Les emplois de l'inclusion",
      img: logoLesEmplois,
    },
    jeVeuxAider: { name: "JeVeuxAider", img: logoJeVeuxAider },
    google: { name: "Google - Ateliers numériques", img: logoGoole },
    serviceCivique: { name: "Service Civique", img: logoServiceCivique },
    monEnfant: { name: "CNAF - Mon enfant.fr", img: logoMonEnfant },
    financesPedagogie: {
      name: "Finances et pédagogie (Caisse d’épargne)",
      img: logoFinancesPedagogie,
    },
    actionLogement: {
      name: "Action Logement",
      img: logoActionLogement,
    },
    ardennes: {
      name: "Conseil Départemental des Ardennes",
      img: logoArdennes,
    },
    caf: {
      name: "Caisse d‘allocations familiales",
      img: logoCAF,
    },
    laReunion: {
      name: "Département de la Réunion",
      img: logoLaReunion,
    },
    poleEmploi: {
      name: "Pôle emploi",
      img: logoPoleEmploi,
    },
  };

  export let imgHeight: "small" | "medium" | undefined = undefined;
  export let partnersToShow: Partner[] = [];
</script>

{#each partnersToShow as partner}
  <li class="text-center">
    <img
      class="m-s0 inline"
      class:max-w-[200px]={imgHeight === "medium"}
      class:max-w-[150px]={imgHeight === "small"}
      src={partner.img}
      alt={partner.name}
    />
  </li>
{/each}
