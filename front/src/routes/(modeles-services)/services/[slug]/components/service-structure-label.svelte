<script lang="ts">
  import HomeSmileLineBuildings from "svelte-remix/HomeSmileLineBuildings.svelte";

  import type { Service } from "$lib/types";
  import { capitalize } from "$lib/utils/misc";

  interface Props {
    service: Service;
  }

  let { service }: Props = $props();

  let isDI = $derived("source" in service);
</script>

<div class="gap-s6 text-f14 text-gray-text flex items-center">
  <HomeSmileLineBuildings size="16" />
  <strong>
    {#if !isDI}
      <a href="/structures/{service.structureInfo.slug}" class="underline"
        >{capitalize(service.structureInfo.name)}</a
      >
    {:else}
      {capitalize(service.structureInfo.name)}
    {/if}
  </strong>
</div>
