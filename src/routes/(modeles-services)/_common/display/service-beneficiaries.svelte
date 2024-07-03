<script lang="ts">
  import Accordion from "$lib/components/display/accordion.svelte";
  import type { Model, Service } from "$lib/types";

  export let service: Service | Model;
</script>

<Accordion title="Qui peut bénéficier de ce service ?">
  <div class="mb-s32">
    <h3>Le public concerné</h3>

    <ul>
      {#if Array.isArray(service.concernedPublicDisplay)}
        {#each service.concernedPublicDisplay as pub (pub)}
          <li>{pub}</li>
        {:else}
          <li>Tous publics</li>
        {/each}
      {:else}
        <li>Non renseigné</li>
      {/if}
    </ul>
  </div>

  <div class="mb-s32">
    <h3>Les critères d’admission</h3>

    <ul>
      {#if Array.isArray(service.accessConditionsDisplay)}
        {#each service.accessConditionsDisplay as condition (condition)}
          <li>{condition}</li>
        {:else}
          {#if !service.qpvOrZrr}
            <li>Aucun</li>
          {/if}
        {/each}
      {:else}
        <li>Non renseigné</li>
      {/if}
      {#if service.qpvOrZrr}
        <li>uniquement QPV ou ZRR</li>
      {/if}
    </ul>
  </div>

  <div class="mb-s32">
    <h3>Les pré-requis, compétences</h3>
    <ul>
      {#if Array.isArray(service.requirementsDisplay)}
        {#each service.requirementsDisplay as reqs}
          <li>{reqs}</li>
        {:else}
          <li>Aucun</li>
        {/each}
      {:else}
        <li>Non renseigné</li>
      {/if}
    </ul>
  </div>
</Accordion>

<style lang="postcss">
  ul {
    @apply mb-s24 list-disc break-all pl-s20 text-f18 leading-32 text-gray-text;
  }
</style>
