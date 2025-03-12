<script lang="ts">
  import HomeSmileLineBuildings from "svelte-remix/HomeSmileLineBuildings.svelte";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import type { Service } from "$lib/types";
  import { capitalize } from "$lib/utils/misc";

  export let service: Service;
  export let isDI: false;

  $: diffusionZoneDetails = service.diffusionZoneDetails
    ? `(${service.diffusionZoneDetails})`
    : "";
  $: diffusionZone = service.diffusionZoneDetailsDisplay
    ? [service.diffusionZoneDetailsDisplay, diffusionZoneDetails]
        .filter(Boolean)
        .join(" ")
    : "Non renseigné";
</script>

<div class="gap-s24 text-gray-text flex flex-col">
  <div>
    <Breadcrumb
      {service}
      structure={service.structureInfo}
      currentLocation="service"
    />
  </div>

  <div class="gap-s16 flex flex-col">
    <div class="gap-s6 text-f14 flex items-center">
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
    <h1 class="mb-s0 mr-s12 text-magenta-dark text-f38 leading-s48">
      {service.name}
    </h1>
    <div class="text-f14">
      Périmètre d’éligibilité&#8239;: {diffusionZone}
    </div>
  </div>
</div>
