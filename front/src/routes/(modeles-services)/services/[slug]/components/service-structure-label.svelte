<script lang="ts">
  import HomeSmileLineBuildings from "svelte-remix/HomeSmileLineBuildings.svelte";

  import { page } from "$app/stores";

  import type { Service } from "$lib/types";
  import { capitalize } from "$lib/utils/misc";

  interface Props {
    service: Service;
  }

  let { service }: Props = $props();

  let isDI = $derived("source" in service);
  // Passe le `searchId` (dans l'URL) vers le détail de la structure afin de
  // rattacher sa consultation à la recherche originale.
  let searchId = $derived($page.url.searchParams.get("searchId"));
</script>

<div class="gap-s6 text-f14 text-gray-text flex items-center">
  <HomeSmileLineBuildings size="16" />
  <strong>
    {#if !isDI}
      <a
        href="/structures/{service.structureInfo.slug}{searchId
          ? `?searchId=${searchId}`
          : ''}"
        class="underline">{capitalize(service.structureInfo.name)}</a
      >
    {:else}
      {capitalize(service.structureInfo.name)}
    {/if}
  </strong>
</div>
