<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import AbTestingSection from "$lib/components/specialized/ab-testing-section.svelte";
  import Favorite from "$lib/components/specialized/favorite-icon.svelte";
  import type { Service } from "$lib/types";
  import { capitalize } from "$lib/utils/misc";

  export let service: Service;
  export let isDI: false;
</script>

<Bookmarkable slug={service.slug} let:onBookmark let:isBookmarked>
  <div
    id="service-header"
    class="relative gap-s16 lg:flex-row-reverse lg:justify-between"
  >
    <div class="mb-s48 print:mb-s0">
      <Breadcrumb
        {service}
        structure={service.structureInfo}
        currentLocation="service"
        {isDI}
      />
    </div>
    <div class="flex items-baseline justify-between">
      <h1 class="mb-s0 mr-s12 leading-[3rem] text-white print:text-france-blue">
        {service.name}
      </h1>

      {#if !isDI}
        <AbTestingSection
          abTestingName="mobilisation"
          showIfGroups={["mobilisation--ancien-design"]}
        >
          <Favorite big on:click={onBookmark} active={isBookmarked} inverted />
        </AbTestingSection>
      {/if}
    </div>
    <div
      class="mb-s48 mt-s16 flex flex-col text-f18 text-white print:text-france-blue md:flex-row md:items-center"
    >
      <div><strong>{capitalize(service.structureInfo.name)}</strong></div>
      {#if !isDI}
        <div
          class="mx-s8 hidden font-bold print:hidden md:block print:md:hidden"
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
      class="mb-s32 flex flex-col text-f18 text-white print:text-france-blue md:flex-row md:items-center"
    >
      <div>
        Périmètre : <strong
          >{service.diffusionZoneDetailsDisplay || "Non renseigné"}</strong
        >
      </div>
    </div>
  </div>
</Bookmarkable>
