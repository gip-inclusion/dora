<script lang="ts">
  import { fly } from "svelte/transition";
  import { starSmileFillIcon, starSmileLineIcon } from "$lib/icons";
  import { CANONICAL_URL } from "$lib/env";
  import { markPenIcon, checkIcon, downloadIcon, linkIcon } from "$lib/icons";
  import type { Service } from "$lib/types";
  import { trackFeedback, trackPrintService } from "$lib/utils/plausible";
  import FeedbackModal from "$lib/components/specialized/services/feedback/feedback-modal.svelte";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import { browser } from "$app/environment";
  import { userInfo } from "$lib/utils/auth";

  export let service: Service;
  export let isDI = false;

  // Suggérer une modification
  let feedbackModalIsOpen = false;

  function handleFeedback() {
    feedbackModalIsOpen = true;
    trackFeedback(service);
  }

  // Partager ce service
  export let copied = false;
  function doCopy() {
    navigator.clipboard.writeText(
      `${CANONICAL_URL}/services/${isDI ? `di/` : ``}${service.slug}`
    );

    copied = true;
    setTimeout(() => (copied = false), 2000);
  }
</script>

{#if !service.canWrite && browser && !isDI}
  <div class="ml-s24 text-f16 text-gray-text print:hidden">
    <FeedbackModal {service} bind:isOpen={feedbackModalIsOpen} />
    <button class="flex hover:text-magenta-cta" on:click={handleFeedback}>
      <span class="mr-s10 h-s24 w-s24 fill-current">
        {@html markPenIcon}
      </span>
      Suggérer une modification
    </button>
  </div>
{/if}

<div class="ml-s24 text-f16 text-gray-text print:hidden">
  <button
    class="flex text-left hover:text-magenta-cta"
    on:click={() => {
      trackPrintService(service);
      print();
    }}
  >
    <span class="mr-s10 h-s24 w-s24 fill-current">
      {@html downloadIcon}
    </span>
    Imprimer ou télécharger en PDF</button
  >
</div>
{#if service.status === "PUBLISHED"}
  <div class="ml-s24 text-f16 text-gray-text print:hidden">
    <button
      class="flex hover:text-magenta-cta"
      title="Copier le lien de ce service"
      on:click={doCopy}
    >
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

      <span class="ml-s32">Copier le lien du service</span>
    </button>
  </div>
{/if}

{#if browser && $userInfo && service.status !== "ARCHIVED"}
  <Bookmarkable slug={service.slug} {isDI} let:onBookmark let:isBookmarked>
    <button
      class="ml-s24 flex text-f16 text-gray-text print:hidden {isBookmarked
        ? 'text-magenta-cta hover:text-gray-text'
        : 'hover:text-magenta-cta'}"
      on:click={onBookmark}
    >
      <span class="h-s24 w-s24 fill-current">
        {@html isBookmarked ? starSmileFillIcon : starSmileLineIcon}
      </span>
      <span class="ml-s10 text-f16">
        {#if isBookmarked}
          Retirer des favoris
        {:else}
          Ajouter aux favoris
        {/if}
      </span>
    </button>
  </Bookmarkable>
{/if}
