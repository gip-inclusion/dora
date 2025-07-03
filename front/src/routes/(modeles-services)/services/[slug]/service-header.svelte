<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import type { Service } from "$lib/types";
  import ServiceStructureLabel from "./components/service-structure-label.svelte";

  interface Props {
    service: Service;
  }

  let { service }: Props = $props();
</script>

<div class="gap-s48 text-gray-text flex flex-col">
  <div>
    <Breadcrumb
      {service}
      structure={service.structureInfo}
      currentLocation="service"
    />
  </div>

  <div class="gap-s16 flex flex-col">
    <ServiceStructureLabel {service} />
    <h1 class="mb-s0 mr-s12 text-magenta-dark text-f38 leading-s48">
      {service.name}
    </h1>
    <div class="text-f14">
      Périmètre d’éligibilité&#8239;: {service.diffusionZoneDetailsDisplay ||
        "non renseigné"}
    </div>
  </div>
</div>
