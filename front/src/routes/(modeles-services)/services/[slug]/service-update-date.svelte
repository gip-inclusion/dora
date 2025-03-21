<script lang="ts">
  import { browser } from "$app/environment";
  import type { Service } from "$lib/types";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import FeedbackModal from "../../_common/display/modals/feedback-modal.svelte";

  export let service: Service;

  let feedbackModalIsOpen = false;

  $: isDI = "source" in service;
</script>

<div class="text-f16">
  <div
    class:text-orange={service.updateNeeded}
    class:text-service-green-darker={!service.updateNeeded}
  >
    <RelativeDateLabel
      date={service.modificationDate}
      prefix="Actualisé"
      bold
    />
  </div>
  {#if !service.canWrite && !isDI}
    <div>
      <button
        class="text-gray-text underline"
        on:click={() => (feedbackModalIsOpen = true)}
        >Signalez-nous toute erreur ou suggestion de modification.</button
      >
    </div>
  {/if}
</div>

{#if browser && !service.canWrite && !isDI}
  <FeedbackModal bind:isOpen={feedbackModalIsOpen} {service} />
{/if}
