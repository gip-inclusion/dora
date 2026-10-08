<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import type { Service } from "$lib/types";
  import ServiceStructureLabel from "./components/service-structure-label.svelte";
  import { NATIONAL_ELIGIBLITITY_ZONE } from "$lib/consts";

  interface Props {
    service: Service;
  }

  let { service }: Props = $props();

  const MAX_ZONES_TO_DISPLAY = 4;

  function formatEligiblityZones() {
    if (
      !service.zoneEligibiliteDisplay ||
      service.zoneEligibiliteDisplay.length === 0
    ) {
      return NATIONAL_ELIGIBLITITY_ZONE;
    }

    let eligibilityZones = service.zoneEligibiliteDisplay.slice(
      0,
      MAX_ZONES_TO_DISPLAY
    );

    let joinedZones = eligibilityZones.map((zone) => zone.label).join(", ");

    if (service.zoneEligibiliteDisplay.length > MAX_ZONES_TO_DISPLAY) {
      joinedZones += " ...";
    }

    return joinedZones;
  }

  const eligibilityZones = formatEligiblityZones();
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
      Périmètre d’éligibilité&#8239;: {eligibilityZones}
    </div>
  </div>
</div>
