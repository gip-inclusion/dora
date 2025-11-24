<script lang="ts">
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";

  import { orientationState } from "./state.svelte.js";

  import OrientationsExportCard from "./orientations-export-card.svelte";
  import DownloadLineSystem from "svelte-remix/DownloadLineSystem.svelte";
  import { CANONICAL_URL } from "$lib/env";
  import type { PageData } from "./$types";

  interface Props {
    data: PageData;
  }
  const { data }: Props = $props();

  const hasOrientations =
    (orientationState.selectedType === "sent" && data.stats.totalSent > 0) ||
    (orientationState.selectedType === "received" &&
      data.stats.totalReceivedPending > 0);
</script>

<EnsureLoggedIn>
  <div>
    <h2>
      {`Orientations ${orientationState.selectedType === "sent" ? "envoyées" : "reçues"}`}
    </h2>
    {#if orientationState.selectedType === "sent"}
      <p>
        <b>{data.stats.totalSentPending} demandes en cours</b> / {data.stats
          .totalSent} envoyées
      </p>
    {:else}
      <p>
        <b>{data.stats.totalReceivedPending} demandes à traiter</b> / {data
          .stats.totalReceived}
        reçues
      </p>
    {/if}
    <OrientationsExportCard
      type={orientationState.selectedType}
      {hasOrientations}
    >
      {#if hasOrientations}
        <DownloadLineSystem class="fill-magenta-cta" /><button
          class="text-magenta-cta">Télécharger la liste</button
        >
      {:else if orientationState.selectedType === "received"}
        <a
          href={`/structures/${data.structure.slug}/services`}
          class="text-magenta-cta">Passer en revue mes services</a
        >
        <button
          class="text-magenta-cta"
          onclick={() =>
            navigator.clipboard.writeText(
              `${CANONICAL_URL}/structures/${data.structure.slug}`
            )}>Copier le lien de ma structure</button
        >
      {:else}
        <a href="/recherche-textuelle" class="text-magenta-cta"
          >Rechercher par mots-clé</a
        >
        <a href="/" class="text-magenta-cta">Rechercher par lieu et besoins</a>
      {/if}
    </OrientationsExportCard>
  </div>
</EnsureLoggedIn>
