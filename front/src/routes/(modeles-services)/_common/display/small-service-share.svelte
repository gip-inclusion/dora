<script lang="ts">
  import { fly } from "svelte/transition";
  import { starSmileFillIcon, starSmileLineIcon } from "$lib/icons";
  import { CANONICAL_URL } from "$lib/env";
  import { markPenIcon, checkIcon, downloadIcon, linkIcon } from "$lib/icons";
  import type { Service } from "$lib/types";
  import FeedbackModal from "./modals/feedback-modal.svelte";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import { browser } from "$app/environment";
  import { userInfo } from "$lib/utils/auth";


  // Suggérer une modification
  let feedbackModalIsOpen = $state(false);

  function handleFeedback() {
    feedbackModalIsOpen = true;
  }

  
  interface Props {
    service: Service;
    isDI?: boolean;
    // Partager ce service
    copied?: boolean;
  }

  let { service, isDI = false, copied = $bindable(false) }: Props = $props();
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
    <button class="hover:text-magenta-cta flex" onclick={handleFeedback}>
      <span class="mr-s10 h-s24 w-s24 fill-current">
        {@html markPenIcon}
      </span>
      Suggérer une modification
    </button>
  </div>
{/if}

<div class="ml-s24 text-f16 text-gray-text print:hidden">
  <button
    class="hover:text-magenta-cta flex text-left"
    onclick={() => {
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
      class="hover:text-magenta-cta flex"
      title="Copier le lien de ce service"
      onclick={doCopy}
    >
      {#if copied}
        <span
          class="h-s24 w-s24 absolute fill-current"
          transition:fly={{ y: 50, duration: 500 }}
        >
          {@html checkIcon}
        </span>
      {:else}
        <span
          class="h-s24 w-s24 absolute fill-current"
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
  <Bookmarkable slug={service.slug} {isDI}  >
    {#snippet children({ onBookmark, isBookmarked })}
        <button
        class="ml-s24 text-f16 text-gray-text flex print:hidden {isBookmarked
          ? 'text-magenta-cta hover:text-gray-text'
          : 'hover:text-magenta-cta'}"
        onclick={onBookmark}
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
          {/snippet}
    </Bookmarkable>
{/if}
