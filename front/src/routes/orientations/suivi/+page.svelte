<script lang="ts">
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";

  import { orientationState } from "./state.svelte.js";

  import OrientationsExportCard from "./orientations-export-card.svelte";
  import DownloadLineSystem from "svelte-remix/DownloadLineSystem.svelte";
  import CheckLineSystem from "svelte-remix/CheckLineSystem.svelte";
  import { CANONICAL_URL } from "$lib/env";
  import type { PageData } from "./$types";
  import { fly } from "svelte/transition";

  interface Props {
    data: PageData;
  }
  const { data }: Props = $props();

  const hasOrientations = $derived(
    (orientationState.selectedType === "sent" && data.stats.totalSent > 0) ||
      (orientationState.selectedType === "received" &&
        data.stats.totalReceived > 0)
  );

  let linkCopied = $state(false);

  function handleCopy() {
    navigator.clipboard.writeText(
      `${CANONICAL_URL}/structures/${data.structure.slug}`
    );
    linkCopied = true;
    setTimeout(() => (linkCopied = false), 2000);
  }
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
      structureHasServices={data.stats.structureHasServices}
    >
      {#if hasOrientations}
        <button class="text-magenta-cta gap-s4 flex flex-row font-bold"
          ><DownloadLineSystem class="fill-magenta-cta" />Télécharger la liste</button
        >
      {:else if orientationState.selectedType === "received" && data.stats.structureHasServices}
        <a
          href={`/structures/${data.structure.slug}/services`}
          class="text-magenta-cta font-bold">Passer en revue mes services</a
        >
        <div class="relative">
          <button class="text-magenta-cta font-bold" onclick={handleCopy}
            >Copier le lien de ma structure</button
          >
          {#if linkCopied}
            <div
              class="ml-s6 absolute top-1/2 left-full -translate-y-1/2"
              transition:fly={{ y: 50, duration: 500 }}
            >
              <CheckLineSystem />
            </div>
          {/if}
        </div>
      {:else if orientationState.selectedType === "received" && !data.stats.structureHasServices}
        <a
          href={`/services/creer?structure=${data.structure.slug}`}
          class="text-magenta-cta font-bold"
          >Référencer un service
        </a>
      {:else}
        <a href="/recherche-textuelle" class="text-magenta-cta font-bold"
          >Rechercher par mots-clé</a
        >
        <a href="/" class="text-magenta-cta font-bold"
          >Rechercher par lieu et besoins</a
        >
      {/if}
    </OrientationsExportCard>
  </div>
</EnsureLoggedIn>
