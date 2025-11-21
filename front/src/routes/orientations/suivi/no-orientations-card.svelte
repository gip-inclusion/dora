<script lang="ts">
  import illuRecenser from "$lib/assets/illustrations/illu-recenser-black-and-white.svg";
  import InboxArchiveLineBusiness from "svelte-remix/InboxArchiveLineBusiness.svelte";
  import InboxUnarchiveLineBusiness from "svelte-remix/InboxUnarchiveLineBusiness.svelte";
  import type { OrientationType } from "./state.svelte";

  interface Props {
    type: OrientationType;
  }

  const CONTENT_BY_TYPE = {
    sent: {
      title: "Aucune demande d'orientation reçue pour le moment",
      text: "Assurez-vous d'avoir activé le formulaire DORA sur vos services. Pour augmenter votre visibilité, partagez le lien de votre structure avec vos partenaires afin qu'ils puissent orienter leurs bénéficiaires vers vos dispositifs via DORA.",
    },
    received: {
      title: "Vous n'avez pas encore réalisé d'orientations",
      text: "Besoin d'orienter des bénéficiaires vers des dispositifs adaptés ? Commencez par identifier les services disponibles selon leurs besoins et votre territoire.",
    },
  };

  const { type }: Props = $props();
</script>

<div class="flex flex-row justify-center border-1 border-dashed">
  <div class="flex flex-col items-center">
    {#if type === "received"}
      <InboxArchiveLineBusiness />
    {:else}
      <InboxUnarchiveLineBusiness />
    {/if}
    <h2>{CONTENT_BY_TYPE[type].title}</h2>
    <h4>
      {CONTENT_BY_TYPE[type].text}
    </h4>
    <div class="gap-s32 flex flex-row justify-center">
      {#if type === "received"}
        <button class="text-magenta-cta">Paser en revue mes services</button>
        <button class="text-magenta-cta">Copier le lien de ma structure</button>
      {:else}
        <a href="recherche" class="text-magenta-cta">Rechercher par mots-clé</a>
        <a href="recherche" class="text-magenta-cta"
          >Rechercher par lieu et besoins</a
        >
      {/if}
    </div>
  </div>
  <img src={illuRecenser} alt="" class="mb-s16 w-full" />
</div>
