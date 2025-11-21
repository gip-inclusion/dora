<script lang="ts">
  import illuRecenser from "$lib/assets/illustrations/illu-recenser-black-and-white.svg";
  import illuModeEmploi from "$lib/assets/illustrations/illu-modeemploi.svg";
  import InboxArchiveLineBusiness from "svelte-remix/InboxArchiveLineBusiness.svelte";
  import InboxUnarchiveLineBusiness from "svelte-remix/InboxUnarchiveLineBusiness.svelte";
  import type { OrientationType } from "./state.svelte";
  import DownloadLineSystem from "svelte-remix/DownloadLineSystem.svelte";

  interface Props {
    type: OrientationType;
    hasOrientations: boolean;
  }

  const CONTENT_BY_TYPE = {
    sent: {
      noOrientations: {
        title: "Aucune demande d'orientation reçue pour le moment",
        text: "Assurez-vous d'avoir activé le formulaire DORA sur vos services. Pour augmenter votre visibilité, partagez le lien de votre structure avec vos partenaires afin qu'ils puissent orienter leurs bénéficiaires vers vos dispositifs via DORA.",
      },
      hasOrientations: {
        title: "Liste des orientations envoyées",
        text: "Téléchargez la liste des orientations envoyées par votre structure. Fichier proposé au format .xls",
      },
    },
    received: {
      noOrientations: {
        title: "Vous n'avez pas encore réalisé d'orientations",
        text: "Besoin d'orienter des bénéficiaires vers des dispositifs adaptés ? Commencez par identifier les services disponibles selon leurs besoins et votre territoire.",
      },
      hasOrientations: {
        title: "Vous avez reçu des orientations",
        text: "Téléchargez la liste des orientations reçues par votre structure. Vous pourrez ainsi consulter et trier ces orientations. Fichier proposé au format .xls",
      },
    },
  };

  const { type, hasOrientations }: Props = $props();
  const contentMapKey = hasOrientations ? "hasOrientations" : "noOrientations";
</script>

<div
  class="px-s20 py-s32 gap-s32 border-gray-03 flex flex-row justify-center border-2 border-dashed text-center"
>
  <div class="gap-s12 flex flex-2 flex-col items-center justify-center">
    {#if type === "received"}
      <InboxArchiveLineBusiness />
    {:else}
      <InboxUnarchiveLineBusiness />
    {/if}
    <h2>{CONTENT_BY_TYPE[type][contentMapKey].title}</h2>
    <h4>
      {CONTENT_BY_TYPE[type][contentMapKey].text}
    </h4>
    <div
      class={[
        "flex flex-row justify-center",
        { "gap-s32": !hasOrientations, "gap-s4": hasOrientations },
      ]}
    >
      {#if hasOrientations}
        <DownloadLineSystem class="fill-magenta-cta" /><button
          class="text-magenta-cta">Télécharger la liste</button
        >
      {:else if type === "received"}
        <button class="text-magenta-cta">Passer en revue mes services</button>
        <button class="text-magenta-cta">Copier le lien de ma structure</button>
      {:else}
        <a href="recherche" class="text-magenta-cta">Rechercher par mots-clé</a>
        <a href="recherche" class="text-magenta-cta"
          >Rechercher par lieu et besoins</a
        >
      {/if}
    </div>
  </div>
  <div class="flex-1">
    {#if hasOrientations}
      <img src={illuModeEmploi} alt="" class="mb-s16 w-full" />
    {:else}
      <img src={illuRecenser} alt="illustration-recenser" />
    {/if}
  </div>
</div>
