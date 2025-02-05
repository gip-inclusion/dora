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
  <div class="mb-s48 print:mb-s0">
    <Breadcrumb
      {service}
      structure={service.structureInfo}
      currentLocation="service"
    />
  </div>
  <h1 class="mb-s0 mr-s12 print:text-france-blue leading-[3rem] text-white">
    {service.name}
  </h1>
  <div
    class="mb-s32 mt-s16 text-f18 print:mb-s8 print:text-france-blue flex flex-col text-white md:flex-row md:items-center"
  >
    <div><strong>{capitalize(service.structureInfo.name)}</strong></div>
    {#if !isDI}
      <div
        class="mx-s8 hidden font-bold md:block print:hidden print:md:hidden"
        aria-hidden="true"
      >
        •
      </div>
      <div class="print:hidden">
        <a
          class="underline"
          href="/structures/{service.structureInfo.slug}/services"
          >Voir les autres services ({service.structureInfo.numServices})</a
        >
      </div>
    {/if}
  </div>

  <div
    class="text-f18 print:text-france-blue text-white md:flex-row md:items-center"
  >
    Périmètre : <strong
      >{service.diffusionZoneDetailsDisplay || "Non renseigné"}</strong
    >
  </div>
</div>
