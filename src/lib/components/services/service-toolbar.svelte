<script>
  import { browser } from "$app/env";

  import { token } from "$lib/auth";

  import Button from "$lib/components/button.svelte";

  import SuggestionModal from "./suggestion-modal.svelte";
  import ServiceMenu from "./service-menu.svelte";
  import StateButtonMenu from "./state-button-menu.svelte";
  import ServiceSync from "./service-sync.svelte";
  export let service, servicesOptions;
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

<div class="inline-flex flex-wrap items-start gap-s8">
  {#if $token && service.canWrite}
    <StateButtonMenu {service} {servicesOptions} {onRefresh} />
    {#if service.model}
      <ServiceSync modelChanged={service.modelChanged}>
        <ServiceMenu {service} {onRefresh} inline />
      </ServiceSync>
    {:else}
      <ServiceMenu {service} {onRefresh} inline />
    {/if}
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
