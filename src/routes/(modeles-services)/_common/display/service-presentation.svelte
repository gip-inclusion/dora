<script lang="ts">
  import AbTestingSection from "$lib/components/specialized/ab-testing-section.svelte";
  import ServiceKeyInformations from "$lib/components/specialized/services/display/new/service-key-informations.svelte";
  import SubcategoryList from "$lib/components/specialized/services/display/old/subcategory-list.svelte";
  import type { Service, ServicesOptions } from "$lib/types";
  import ServiceDescription from "../service-description.svelte";

  export let service: Service;
  export let servicesOptions: ServicesOptions;
</script>

<h2 class="mb-s40">Présentation du service</h2>

<p class="mb-s40 font-bold">
  {service.shortDesc}
</p>

<AbTestingSection
  abTestingName="mobilisation"
  showIfGroups={["mobilisation--ancien-design"]}
>
  <div class="mb-s40">
    <h3 class="text-f17">Ce service répond aux besoins</h3>
    <SubcategoryList {service} {servicesOptions} />
  </div>

  <div class="mb-s40">
    <h3>Type de service</h3>
    <ul class="inline-flex flex-wrap text-f18 text-gray-text">
      {#each service.kindsDisplay as kind, index (kind)}
        <li class:separator={index > 0}>{kind}</li>
      {/each}
    </ul>
  </div>
</AbTestingSection>

<AbTestingSection
  abTestingName="mobilisation"
  showIfGroups={["mobilisation--fond-bleu", "mobilisation--fond-blanc"]}
>
  <div class="rounded-lg border border-gray-02 p-s32 pb-s48">
    <ServiceKeyInformations {service} {servicesOptions} />
  </div>
</AbTestingSection>

<div class="mb-s40" />

{#if service.fullDesc}
  <div class="mb-s40">
    <h3>Description du service</h3>
    <ServiceDescription {service} />
  </div>
{/if}

<style lang="postcss">
  li.separator::before {
    content: "•";
    @apply mx-s6;
  }
</style>
