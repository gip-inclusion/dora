<script lang="ts">
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";

  import { orientationState } from "./state.svelte.js";

  import OrientationsExportCard from "./orientations-export-card.svelte";
  import ExportWarningModal from "./export-warning-modal.svelte";
  import OrientationsStatsDisplay from "./orientations-stats-display.svelte";
  import DownloadLineSystem from "svelte-remix/DownloadLineSystem.svelte";
  import CheckLineSystem from "svelte-remix/CheckLineSystem.svelte";
  import { CANONICAL_URL } from "$lib/env";
  import type { PageData } from "./$types";
  import { fly } from "svelte/transition";
  import { toast } from "@zerodevx/svelte-toast";
  import Notice from "$lib/components/display/notice.svelte";
  import { requestOrientationExportLink } from "$lib/requests/orientations";
  import { userInfo } from "$lib/utils/auth";
  import { logException } from "$lib/utils/logger";
  import { ORIENTATIONS_EXPORT_LINK_VALIDITY_MINUTES } from "$lib/consts";

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

  let isModalOpen = $state(false);

  const toggleModal = () => {
    isModalOpen = !isModalOpen;
  };

  let isSendingLink = $state(false);
  let linkSent = $state(false);

  const handleModalSubmit = async () => {
    isSendingLink = true;
    linkSent = false;
    let ok = false;
    try {
      ({ ok } = await requestOrientationExportLink(
        data.structure.slug,
        orientationState.selectedType
      ));
    } catch (err) {
      logException(err);
    }
    isSendingLink = false;
    toggleModal();

    if (ok) {
      linkSent = true;
    } else {
      toast.push(
        "Une erreur est survenue lors de l’envoi du lien de téléchargement."
      );
    }
  };
</script>

<EnsureLoggedIn>
  <div>
    {#if linkSent}
      <div class="mb-s24">
        <Notice type="success" title="Envoi validé">
          <p class="text-f14 mb-s0">
            Le lien de téléchargement sécurisé a été envoyé à votre adresse mail
            {$userInfo?.email}. Il est valable
            {ORIENTATIONS_EXPORT_LINK_VALIDITY_MINUTES} minutes.
          </p>
        </Notice>
      </div>
    {/if}
    <h2>
      {`Orientations ${orientationState.selectedType === "sent" ? "envoyées" : "reçues"}`}
    </h2>
    <OrientationsStatsDisplay stats={data.stats} />
    <OrientationsExportCard
      {hasOrientations}
      structureHasServices={data.stats.structureHasServices}
    >
      {#if hasOrientations}
        <button
          onclick={toggleModal}
          class="text-magenta-cta gap-s4 flex flex-row font-bold"
          ><DownloadLineSystem class="fill-magenta-cta" />Télécharger la liste</button
        >
      {:else if orientationState.selectedType === "received" && data.stats.structureHasServices}
        <a
          id="service-review-link"
          href={`/structures/${data.structure.slug}/services`}
          class="text-magenta-cta font-bold">Passer en revue mes services</a
        >
        <div class="relative">
          <button
            id="structure-copy-button"
            class="text-magenta-cta font-bold"
            onclick={handleCopy}>Copier le lien de ma structure</button
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
          id="service-reference-link"
          href={`/services/creer?structure=${data.structure.slug}`}
          class="text-magenta-cta font-bold"
          >Référencer un service
        </a>
      {:else}
        <a
          id="text-search-link"
          href="/recherche-textuelle"
          class="text-magenta-cta font-bold">Rechercher par mots-clé</a
        >
        <a id="keyword-search-link" href="/" class="text-magenta-cta font-bold"
          >Rechercher par lieu et besoins</a
        >
      {/if}
    </OrientationsExportCard>
  </div>
  <ExportWarningModal
    isOpen={isModalOpen}
    handleClose={toggleModal}
    handleSubmit={handleModalSubmit}
    isSubmitting={isSendingLink}
  />
</EnsureLoggedIn>
