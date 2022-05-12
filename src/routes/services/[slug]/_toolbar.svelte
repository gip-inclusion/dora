<script>
  import { browser } from "$app/env";

  import { token } from "$lib/auth";
  import Button from "$lib/components/button.svelte";

  import SuggestionModal from "./_suggestion-modal.svelte";
  import Menu from "$lib/components/services/menu.svelte";

  export let service;
  export let onRefresh;

  let suggestionModalIsOpen = false;
  function handleSuggestion() {
    suggestionModalIsOpen = true;
    if (browser) {
      plausible("suggestion", {
        props: {
          service: service.name,
          slug: service.slug,
          structure: service.structureInfo.name,
          departement: service.department,
        },
      });
    }
  }
</script>

<div class="inline-flex flex-wrap gap-s8">
  {#if $token && service.canWrite}
    <Menu {service} secondary {onRefresh} />
  {:else}
    <SuggestionModal {service} bind:isOpen={suggestionModalIsOpen} />
    <Button
      label="Suggérer une modification"
      secondary
      small
      on:click={handleSuggestion}
    />
  {/if}
</div>
