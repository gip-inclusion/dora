<script lang="ts">
  import Tag from "$lib/components/display/tag.svelte";

  import { EMPLOIS_PORTAL_PAGE_URL } from "$lib/env";

  import type { NexusServiceID } from "$lib/requests/nexus";

  export type NexusService = {
    id: NexusServiceID;
    label: string;
    url: string;
    icon: string;
  };
  interface Props {
    service: NexusService;
    activated?: boolean;
    activable?: boolean;
  }

  let { service, activated = false, activable = false }: Props = $props();

  let url = $derived(
    activated ? service.url : `${EMPLOIS_PORTAL_PAGE_URL}/service/${service.id}`
  );
</script>

<a
  href={url}
  target="_blank"
  rel="noopener"
  class="w-s344 p-s12 text-gray-text hover:bg-magenta-10 flex items-center justify-between rounded-sm"
>
  <img src={service.icon} alt={service.label} class="h-s40" />
  {#if activated}
    <Tag variant="success">Activé</Tag>
  {:else if activable}
    <Tag variant="info">Activable en 1 clic</Tag>
  {/if}
</a>
