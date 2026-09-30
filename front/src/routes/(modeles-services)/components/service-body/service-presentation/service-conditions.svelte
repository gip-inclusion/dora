<script lang="ts">
  import Calendar2LineBusiness from "svelte-remix/Calendar2LineBusiness.svelte";
  import ChatCheckFillCommunication from "svelte-remix/ChatCheckFillCommunication.svelte";
  import MapPin2FillMap from "svelte-remix/MapPin2FillMap.svelte";

  import type { Model, Service } from "$lib/types";
  import { isDurationValid } from "$lib/utils/service";

  import ServiceCard from "./components/service-card.svelte";
  import ServiceField from "./components/service-field.svelte";
  import ServiceKeyInformationSection from "./service-key-informations/service-key-information-section.svelte";
  import OsmHours from "$lib/components/specialized/osm-hours.svelte";

  interface Props {
    service: Service | Model;
  }

  let { service }: Props = $props();

  const locationKinds = service.isModel
    ? null
    : service.locationKindsDisplay?.join(" · ");

  const addressLine = service.isModel ? null : service.addressLine;

  const weeks = service.durationWeeks ?? 0;
  const duration = isDurationValid(service)
    ? `${service.durationWeeklyHours}h par semaine, pendant ${weeks} semaine${weeks > 1 ? "s" : ""}`
    : null;

  const hasLocation = Boolean(addressLine || service.horairesAccueil);
</script>

{#if locationKinds || duration || hasLocation}
  <ServiceCard title="Conditions d’accueil" divided>
    {#if locationKinds}
      <ServiceKeyInformationSection
        icon={ChatCheckFillCommunication}
        title="Modes d’accueil"
      >
        <p>{locationKinds}</p>
      </ServiceKeyInformationSection>
    {/if}

    {#if duration}
      <ServiceKeyInformationSection
        icon={Calendar2LineBusiness}
        title="Durée de la prestation"
      >
        <p>{duration}</p>
      </ServiceKeyInformationSection>
    {/if}

    {#if hasLocation}
      <ServiceKeyInformationSection
        icon={MapPin2FillMap}
        title="Lieu d’accueil"
      >
        <div class="gap-s16 flex flex-col">
          {#if addressLine}
            <ServiceField title="Adresse du lieu">
              <p>{addressLine}</p>
            </ServiceField>
          {/if}
          {#if service.horairesAccueil}
            <ServiceField title="Horaires d’ouverture du service">
              <OsmHours osmHours={service.horairesAccueil} />
            </ServiceField>
          {/if}
        </div>
      </ServiceKeyInformationSection>
    {/if}
  </ServiceCard>
{/if}
