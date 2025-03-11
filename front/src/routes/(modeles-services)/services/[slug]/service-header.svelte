<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import type { Service } from "$lib/types";
  import { capitalize } from "$lib/utils/misc";

  export let service: Service;
  export let isDI: false;
</script>

<div
  id="service-header"
  class="gap-s16 print:gap-s0 relative lg:flex-row-reverse lg:justify-between"
>
  <div class="mb-s24 print:mb-s0">
    <Breadcrumb
      {service}
      structure={service.structureInfo}
      currentLocation="service"
      dark
    />
  </div>
  <h1 class="mb-s0 mr-s12 text-france-blue text-f38 leading-[3rem]">
    {service.name}
  </h1>
  <div
    class="mb-s32 mt-s16 text-f14 print:mb-s8 print:text-france-blue text-gray-text flex flex-col md:flex-row md:items-center"
  >
    <div>
      <strong
        >{#if !isDI}
          <a href="/structures/{service.structureInfo.slug}" class="underline"
            >{capitalize(service.structureInfo.name)}</a
          >
        {:else}
          {capitalize(service.structureInfo.name)}
        {/if}
      </strong>
      à {service.structureInfo.city} ({service.structureInfo.department})
    </div>
  </div>

  <div
    class="text-f18 print:text-france-blue text-gray-text md:flex-row md:items-center"
  >
    Périmètre : <strong
      >{service.diffusionZoneDetailsDisplay || "Non renseigné"}</strong
    >
  </div>
</div>
