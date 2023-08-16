<script lang="ts">
  import ServiceKeyInformations from "$lib/components/specialized/services/display/service-key-informations.svelte";
  import type { Service, ServicesOptions } from "$lib/types";
  import Notice from "$lib/components/display/notice.svelte";

  import ServiceDescription from "../service-description.svelte";

  export let service: Service;
  export let servicesOptions: ServicesOptions;
  export let isDI = false;
</script>

<h2 class="mb-s40">Présentation du service</h2>

<p class="mb-s40 font-bold">
  {service.shortDesc || ""}
</p>

<div class="rounded-lg border border-gray-02 p-s32 pb-s48">
  <ServiceKeyInformations {service} {servicesOptions} />
</div>

<div class="mb-s40" />

{#if service.fullDesc}
  <div class="mb-s40">
    <h3>Description du service</h3>
    <ServiceDescription {service} />
  </div>
{/if}

{#if isDI}
  <Notice
    title="Ce service provient de {service.source}, via data·inclusion"
    type="info"
  >
    <p class="text-f14">
      Ce service est automatiquement récupéré depuis le référentiel commun
      data·inclusion, auquel participe DORA. Les informations peuvent être
      partielles et certaines fonctionnalités peuvent être indisponibles. Il
      s'agit d’une expérimentation en cours, n'hésitez pas à <a
        class="underline"
        href="https://tally.so/r/nrBNqv ">nous faire part de vos retours</a
      >.
    </p>
  </Notice>
{/if}
