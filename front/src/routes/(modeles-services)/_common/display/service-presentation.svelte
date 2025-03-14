<script lang="ts">
  import ServiceDocuments from "$lib/components/specialized/services/display/service-documents.svelte";
  import ServiceKeyInformations from "$lib/components/specialized/services/display/service-key-informations.svelte";
  import ServiceOtherInformations from "$lib/components/specialized/services/display/service-other-informations.svelte";
  import ServiceSteps from "$lib/components/specialized/services/display/service-steps.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";

  import ServiceDescription from "../service-description.svelte";

  export let service: Service | Model;
  export let servicesOptions: ServicesOptions;
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

  <ServiceDocuments {service} />

  <ServiceOtherInformations {service} {servicesOptions} />
</div>
