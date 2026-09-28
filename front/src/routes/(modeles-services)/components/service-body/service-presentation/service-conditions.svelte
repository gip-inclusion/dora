<script lang="ts">
  import Calendar2LineBusiness from "svelte-remix/Calendar2LineBusiness.svelte";
  import ChatCheckFillCommunication from "svelte-remix/ChatCheckFillCommunication.svelte";
  import MapPin2FillMap from "svelte-remix/MapPin2FillMap.svelte";

  import type { Model, Service } from "$lib/types";
  import { isDurationValid } from "$lib/utils/service";

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
  <section>
    <h2 class="text-f23 text-france-blue mb-s16 leading-32 font-bold">
      Conditions d’accueil
    </h2>

    <div
      class="border-gray-02 p-s32 gap-s32 divide-gray-01 text-f16 text-gray-text [&_p]:mb-s0 [&_p]:text-f16 flex flex-col divide-y rounded-2xl border leading-24 [&_p]:leading-24"
    >
      {#if locationKinds}
        <div class:pb-s32={duration || hasLocation}>
          <ServiceKeyInformationSection
            icon={ChatCheckFillCommunication}
            title="Modes d’accueil"
          >
            <p>{locationKinds}</p>
          </ServiceKeyInformationSection>
        </div>
      {/if}

      {#if duration}
        <div class:pb-s32={hasLocation}>
          <ServiceKeyInformationSection
            icon={Calendar2LineBusiness}
            title="Durée de la prestation"
          >
            <p>{duration}</p>
          </ServiceKeyInformationSection>
        </div>
      {/if}

      {#if hasLocation}
        <div>
          <ServiceKeyInformationSection
            icon={MapPin2FillMap}
            title="Lieu d’accueil"
          >
            <div class="gap-s16 flex flex-col">
              {#if addressLine}
                <div>
                  <h4
                    class="text-f16 text-gray-dark mb-s4 leading-24 font-bold"
                  >
                    Adresse du lieu
                  </h4>
                  <p>{addressLine}</p>
                </div>
              {/if}
              {#if service.horairesAccueil}
                <div>
                  <h4
                    class="text-f16 text-gray-dark mb-s4 leading-24 font-bold"
                  >
                    Horaires d’ouverture du service
                  </h4>
                  <OsmHours osmHours={service.horairesAccueil} />
                </div>
              {/if}
            </div>
          </ServiceKeyInformationSection>
        </div>
      {/if}
    </div>
  </section>
{/if}
