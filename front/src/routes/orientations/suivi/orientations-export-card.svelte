<script lang="ts">
  import illuRecenser from "$lib/assets/illustrations/illu-recenser-black-and-white.svg";
  import illuModeEmploi from "$lib/assets/illustrations/illu-modeemploi.svg";
  import InboxArchiveLineBusiness from "svelte-remix/InboxArchiveLineBusiness.svelte";
  import InboxUnarchiveLineBusiness from "svelte-remix/InboxUnarchiveLineBusiness.svelte";
  import type { OrientationType } from "./state.svelte";
  import type { Snippet } from "svelte";

  interface Props {
    type: OrientationType;
    hasOrientations: boolean;
    structureHasServices: boolean;
    children: Snippet;
  }

  const CONTENT_BY_TYPE = {
    sent: {
      noOrientations: {
        title: "Vous n'avez pas encore réalisé d’orientations",
        text: "Besoin d’orienter des bénéficiaires vers des dispositifs adaptés ? Commencez par identifier les services disponibles selon leurs besoins et votre territoire.",
      },
      hasOrientations: {
        title: "Liste des orientations envoyées",
        text: "Téléchargez la liste des orientations envoyées par votre structure. Fichier proposé au format .xls",
      },
    },
    received: {
      noOrientationsAndServices: {
        title: "Aucune demande d’orientation reçue pour le moment",
        text: "Assurez-vous d’avoir activé le formulaire DORA sur vos services. Pour augmenter votre visibilité, partagez le lien de votre structure avec vos partenaires afin qu’ils puissent orienter leurs bénéficiaires vers vos dispositifs via DORA.",
      },
      noOrientationsAndNoServices: {
        title: "Aucune demande d’orientation reçue pour le moment",
        text: "Pour recevoir des orientations, vous devez d’abord référencer vos services ! Si vous proposez des dispositifs, ajoutez-les sur DORA pour que vos partenaires puissent y orienter leurs bénéficiaires.",
      },
      hasOrientations: {
        title: "Vous avez reçu des orientations",
        text: "Téléchargez la liste des orientations reçues par votre structure. Vous pourrez ainsi consulter et trier ces orientations. Fichier proposé au format .xls",
      },
    },
  };

  const { type, hasOrientations, structureHasServices, children }: Props =
    $props();

  function getContentMapKey() {
    if (type === "sent") {
      return hasOrientations ? "hasOrientations" : "noOrientations";
    }
    if (hasOrientations) {
      return "hasOrientations";
    }
    if (structureHasServices) {
      return "noOrientationsAndServices";
    }
    return "noOrientationsAndNoServices";
  }

  const title = $derived(CONTENT_BY_TYPE[type][getContentMapKey()].title);
  const text = $derived(CONTENT_BY_TYPE[type][getContentMapKey()].text);
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
    <h2 class="text-gray-text">{title}</h2>
    <p>{text}</p>
    <div
      class={[
        "flex flex-row justify-center",
        { "gap-s32": !hasOrientations, "gap-s4": hasOrientations },
      ]}
    >
      {@render children()}
    </div>
  </div>
  <div class="hidden flex-1 md:flex">
    {#if hasOrientations}
      <img src={illuModeEmploi} alt="" class="mb-s16 w-full" />
    {:else}
      <img src={illuRecenser} alt="" />
    {/if}
  </div>
</div>
