<script lang="ts">
  import type { Model, Service, ServicesOptions } from "$lib/types";

  import ServiceDocuments from "./service-documents.svelte";
  import ServiceKeyInformations from "./service-key-informations/service-key-informations.svelte";
  import ServiceOtherInformations from "./service-other-informations.svelte";
  import ServiceSteps from "./service-steps.svelte";

  export let service: Service | Model;
  export let servicesOptions: ServicesOptions;
</script>

<div class="gap-s36 flex flex-col">
  <ServiceKeyInformations {service} {servicesOptions} />

  <ServiceSteps {service} />

  <ServiceDocuments {service} />

  <ServiceOtherInformations {service} {servicesOptions} />
</div>
