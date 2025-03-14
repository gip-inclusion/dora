<script lang="ts">
  import { page } from "$app/stores";
  import ServiceKeyInformations from "$lib/components/specialized/services/display/service-key-informations.svelte";
  import ServiceSteps from "$lib/components/specialized/services/display/service-steps.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import Notice from "$lib/components/display/notice.svelte";

  import ServiceDescription from "../service-description.svelte";

  export let service: Service | Model;
  export let servicesOptions: ServicesOptions;
  export let isDI = false;
</script>

<div class="gap-s36 flex flex-col">
  <div>
    <p class="text-f16 leading-s32 text-gray-text">
  {service.shortDesc || ""}
</p>
    {#if service.fullDesc}
      <ServiceDescription {service} />
    {/if}
  <ServiceKeyInformations {service} {servicesOptions} />
</div>

  <ServiceSteps {service} />
<div class="mb-s40 print:mb-s24" />

{#if isDI}
  <Notice
    title="Ce service provient de {service.source}, via data·inclusion"
    type="info"
  >
    <p class="text-f14">
      Ce service est automatiquement récupéré depuis le référentiel commun
      data·inclusion, auquel participe DORA. N’hésitez pas à <a
        class="underline"
        href="https://tally.so/r/nrBNqv?url={encodeURIComponent(
          $page.url.origin + $page.url.pathname
        )}">nous faire part de vos retours</a
      > si vous remarquez des erreurs.
    </p>
  </Notice>
{/if}
