<script lang="ts">
  import { page } from "$app/stores";
  import ServiceKeyInformations from "$lib/components/specialized/services/display/service-key-informations.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import Notice from "$lib/components/display/notice.svelte";

  import ServiceDescription from "../service-description.svelte";

  interface Props {
    service: Service | Model;
    servicesOptions: ServicesOptions;
    isDI?: boolean;
  }

  let { service, servicesOptions, isDI = false }: Props = $props();
</script>

<h2 class="mb-s40">Présentation du service</h2>

<p class="mb-s40 font-bold">
  {service.shortDesc || ""}
</p>

<div class=" border-gray-02 p-s32 pb-s48 rounded-3xl border">
  <ServiceKeyInformations {service} {servicesOptions} />
</div>

<div class="mb-s40 print:mb-s24"></div>

{#if service.fullDesc}
  <div>
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
      data·inclusion, auquel participe DORA. N’hésitez pas à <a
        class="underline"
        href="https://tally.so/r/nrBNqv?url={encodeURIComponent(
          $page.url.origin + $page.url.pathname
        )}">nous faire part de vos retours</a
      > si vous remarquez des erreurs.
    </p>
  </Notice>
{/if}
