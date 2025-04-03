<script lang="ts">
  import type { Model, Service } from "$lib/types";

  export let service: Service | Model;

  $: isDI = "source" in service;
</script>

{#if !service.canWrite && !isDI}
  <div>
    <button class="text-gray-text underline" on:click
      >Signalez-nous toute erreur ou suggestion de modification.</button
    >
  </div>
{/if}
