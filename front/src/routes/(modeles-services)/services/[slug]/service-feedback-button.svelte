<script lang="ts">
  import type { Model, Service } from "$lib/types";

  export let service: Service | Model;
</script>

{#if !service.canWrite}
  <div>
    <button class="text-gray-text underline" on:click
      >Signalez-nous toute erreur ou suggestion de modification.</button
    >
  </div>
{/if}
