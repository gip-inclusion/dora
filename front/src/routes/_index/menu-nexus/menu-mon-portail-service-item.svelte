<script lang="ts">
  import Tag from "$lib/components/display/tag.svelte";

  import { EMPLOIS_PORTAL_PAGE_URL } from "$lib/env";

  import { trackMatomoEvent } from "$lib/utils/matomo";

  import type { NexusService } from "./consts";

  interface Props {
    service: NexusService;
    activated?: boolean;
    activableInOneClick?: boolean;
  }

  let {
    service,
    activated = false,
    activableInOneClick = false,
  }: Props = $props();

  let url = $derived(
    activated ? service.url : `${EMPLOIS_PORTAL_PAGE_URL}/service/${service.id}`
  );

  function handleClick() {
    trackMatomoEvent({
      category: "Nexus",
      action: activated ? "portail-acceder-service" : "portail-activer-service",
      name: service.id,
    });
  }
</script>

<a
  href={url}
  onclick={handleClick}
  target="_blank"
  rel="noopener"
  class="w-s344 p-s12 text-gray-text hover:bg-magenta-10 flex items-center justify-between rounded-sm"
>
  <img src={service.icon} alt={service.label} class="h-s40" />
  {#if activated}
    <Tag variant="success">Activé</Tag>
  {:else if activableInOneClick}
    <Tag variant="info">Activable en 1 clic</Tag>
  {/if}
</a>
