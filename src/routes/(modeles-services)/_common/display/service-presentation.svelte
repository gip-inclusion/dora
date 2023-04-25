<script lang="ts">
  import type { Service, ServicesOptions } from "$lib/types";
  import ServiceDescription from "../service-description.svelte";
  import SubcategoryList from "./subcategory-list.svelte";

  export let service: Service;
  export let servicesOptions: ServicesOptions;
</script>

<h2 class="mb-s40">Présentation du service</h2>

<p class="mb-s40 font-bold">
  {service.shortDesc}
</p>

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
