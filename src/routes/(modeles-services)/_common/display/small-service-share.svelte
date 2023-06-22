<script lang="ts">
  import { fly } from "svelte/transition";
  import { PDF_SERVICE_URL, CANONICAL_URL } from "$lib/env";
  import { markPenIcon, checkIcon, downloadIcon, linkIcon } from "$lib/icons";
  import type { Service } from "$lib/types";
  import { trackFeedback, trackPDFDownload } from "$lib/utils/plausible";
  import FeedbackModal from "$lib/components/specialized/services/feedback/feedback-modal.svelte";
  import FavoriteIcon from "$lib/components/specialized/favorite-icon.svelte";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import { browser } from "$app/environment";

  export let service: Service;

  // PDF
  export let pdfUrl = `${PDF_SERVICE_URL}/print/?page=${encodeURIComponent(
    `/services/${service.slug}`
  )}&name=${service.slug}.pdf`;

  // Suggérer une modification
  let feedbackModalIsOpen = false;

  function handleFeedback() {
    feedbackModalIsOpen = true;
    trackFeedback(service);
  }

  // Partager ce service
  export let copied = false;
  function doCopy() {
    navigator.clipboard.writeText(`${CANONICAL_URL}/services/${service.slug}`);

    copied = true;
    setTimeout(() => (copied = false), 2000);
  }
</script>

{#if !service.canWrite && browser}
  <div class="ml-s24 text-f16 text-gray-text print:hidden">
    <FeedbackModal {service} bind:isOpen={feedbackModalIsOpen} />
    <button class="flex" on:click={handleFeedback}>
      <span class="mr-s10 h-s24 w-s24 fill-current">
        {@html markPenIcon}
      </span>
      Suggérer une modification
    </button>
  </div>
{/if}

{#if service.status === "PUBLISHED"}
  <div class="ml-s24 text-f16 text-gray-text print:hidden">
    <!-- Le `nofollow` est important ici, on ne veut pas que les robots provoquent la génération des PDFs -->
    <a
      href={pdfUrl}
      class="flex"
      on:click={() => trackPDFDownload(service)}
      rel="nofollow"
    >
      <span class="mr-s10 h-s24 w-s24 fill-current">
        {@html downloadIcon}
      </span>
      Télécharger la fiche au format PDF
    </a>
  </div>

  <div class="ml-s24 text-f16 text-gray-text print:hidden">
    <button class="flex" title="Copier le lien de ce service" on:click={doCopy}>
      {#if copied}
        <span
          class="absolute h-s24 w-s24 fill-current"
          transition:fly={{ y: 50, duration: 500 }}
        >
          {@html checkIcon}
        </span>
      {:else}
        <span
          class="absolute h-s24 w-s24 fill-current"
          transition:fly={{ y: 50, duration: 500 }}
        >
          {@html linkIcon}
        </span>
      {/if}

      <span class="ml-s32">Partager ce service</span>
    </button>
  </div>
{/if}

{#if browser}
  <Bookmarkable slug={service.slug} let:onBookmark let:isBookmarked>
    <button
      class="ml-s24 flex text-f16 text-gray-text print:hidden"
      on:click={onBookmark}
    >
      <FavoriteIcon active={isBookmarked} />
      <span class="ml-s10 text-f16" class:text-france-blue={isBookmarked}>
        {#if isBookmarked}
          Retirer des favoris
        {:else}
          Ajouter aux favoris
        {/if}
      </span>
    </button>
  </Bookmarkable>
{/if}
