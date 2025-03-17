<script lang="ts">
  import CalendarTodoFillBusiness from "svelte-remix/CalendarTodoFillBusiness.svelte";
  import CheckboxCircleFillSystem from "svelte-remix/CheckboxCircleFillSystem.svelte";
  import Compass3FillMap from "svelte-remix/Compass3FillMap.svelte";
  import ErrorWarningFillSystem from "svelte-remix/ErrorWarningFillSystem.svelte";
  import GroupFillUserFaces from "svelte-remix/GroupFillUserFaces.svelte";
  import InformationFillSystem from "svelte-remix/InformationFillSystem.svelte";
  import MapPin2FillMap from "svelte-remix/MapPin2FillMap.svelte";
  import MoneyEuroCircleFillFinance from "svelte-remix/MoneyEuroCircleFillFinance.svelte";
  import TimeFillSystem from "svelte-remix/TimeFillSystem.svelte";

  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getLabelFromValue } from "$lib/utils/choice";
  import { shortenString } from "$lib/utils/misc";
  import { isValidformatOsmHours } from "$lib/utils/opening-hours";
  import { isNotFreeService, isDurationValid } from "$lib/utils/service";

  import OsmHours from "../../osm-hours.svelte";
  import ServiceDuration from "./service-duration.svelte";
  import ServiceKeyInformationLabel from "./service-key-information-label.svelte";
  import ServiceKeyInformationSection from "./service-key-information-section.svelte";

  export let service: Service | Model;
  export let servicesOptions: ServicesOptions;

  $: isDI = "source" in service;

  $: isNotCumulative = !service.isCumulative;
  $: hasFundingLabels = service.fundingLabelsDisplay.length > 0;
  $: isQpvOrZrr = service.qpvOrZrr;
</script>

<section>
  <h2 class="sr-only">Informations clés</h2>

  <div
    class="border-gray-02 p-s32 gap-s32 divide-gray-01 text-f16 text-gray-text flex flex-col divide-y rounded-2xl border leading-24"
  >
    <div class="pb-s32">
      <ServiceKeyInformationSection
        icon={GroupFillUserFaces}
        title="Le public concerné"
      >
        <ul
          class="[&>li+li]:before:mx-s6 [&>li]:inline [&>li+li]:before:inline [&>li+li]:before:content-['·']"
        >
          {#each service.concernedPublicDisplay as pub}
            <li>{pub}</li>
          {:else}
            <li>Tous publics</li>
          {/each}
        </ul>
      </ServiceKeyInformationSection>
    </div>
    <div class="pb-s32">
      <ServiceKeyInformationSection
        icon={CheckboxCircleFillSystem}
        title="Les critéres d’admission"
      >
        {#if Array.isArray(service.accessConditionsDisplay) || service.qpvOrZrr}
          <ul class="list-inside list-disc">
            {#if Array.isArray(service.accessConditionsDisplay)}
              {#each service.accessConditionsDisplay as condition (condition)}
                <li>{condition}</li>
              {:else}
                {#if !service.qpvOrZrr}
                  <li>Aucun critère d’admission spécifique</li>
                {/if}
              {/each}
            {/if}
            {#if service.qpvOrZrr}
              <li>Uniquement QPV ou ZRR</li>
            {/if}
          </ul>
        {:else}
          <li>Aucun détail n'a été renseigné par la structure</li>
        {/if}
      </ServiceKeyInformationSection>
    </div>
    <div class="pb-s32 gap-s32 flex flex-col sm:flex-row">
      {#if !service.isModel}
        <div class="flex-1">
          <div>
            <ServiceKeyInformationSection
              icon={MapPin2FillMap}
              title="Lieu d’accueil"
            >
              {#if service.locationKinds.length > 0}
                <div class="gap-s12 flex flex-col">
                  {#if service.locationKinds.includes("en-presentiel")}
                    <div class="flex flex-col">
                      <strong>Présentiel</strong>
                      {#if service.addressLine}
                        <address class="not-italic">
                          {service.addressLine}
                        </address>
                        <a
                          class="text-magenta-cta mt-s4 font-bold"
                          href={`https://www.openstreetmap.org/search?query=${encodeURIComponent(service.addressLine)}`}
                          target="_blank"
                          rel="noopener ugc">Voir sur la carte</a
                        >
                      {/if}
                    </div>
                  {/if}
                  {#if service.locationKinds.includes("a-distance")}
                    <div class="flex flex-col">
                      <strong
                        >À distance{service.locationKinds.includes(
                          "en-presentiel"
                        )
                          ? " également"
                          : ""}</strong
                      >
                      {#if service.remoteUrl}
                        <a
                          class="text-magenta-cta mt-s4 font-bold"
                          href={service.remoteUrl}
                          target="_blank"
                          rel="noopener ugc"
                        >
                          {shortenString(service.remoteUrl, 35)}
                        </a>
                      {/if}
                    </div>
                  {/if}
                </div>
              {:else}
                Non renseigné
              {/if}
            </ServiceKeyInformationSection>
          </div>
          <div class="mt-s28">
            <ServiceKeyInformationSection
              icon={Compass3FillMap}
              title="Périmètres géographiques"
            >
              {service.diffusionZoneDetailsDisplay}
            </ServiceKeyInformationSection>
          </div>
        </div>
      {/if}
      {#if service.recurrence}
        <div class="flex-1">
          <ServiceKeyInformationSection
            icon={TimeFillSystem}
            title="Fréquence et horaires"
          >
            {#if isDI && isValidformatOsmHours(service.recurrence)}
              <OsmHours osmHours={service.recurrence} />
            {:else}
              {service.recurrence}
            {/if}
          </ServiceKeyInformationSection>
        </div>
      {/if}
    </div>
    {#if isDurationValid(service)}
      <div class="pb-s32">
        <ServiceKeyInformationSection
          icon={CalendarTodoFillBusiness}
          title="Durée de la prestation"
        >
          <ServiceDuration {service} />
        </ServiceKeyInformationSection>
      </div>
    {/if}
    <div class:pb-s32={isNotCumulative || hasFundingLabels || isQpvOrZrr}>
      <ServiceKeyInformationSection
        icon={MoneyEuroCircleFillFinance}
        title="Frais à charge"
      >
        <div class="flex flex-col">
          <span
            class={service.feeCondition &&
            isNotFreeService(service.feeCondition)
              ? "text-warning font-bold"
              : ""}
          >
            {getLabelFromValue(
              service.feeCondition,
              servicesOptions.feeConditions
            )}
          </span>
          <span>
            {#if service.feeDetails}
              {service.feeDetails}
            {:else}
              La structure n’a pas précisé le montant des frais
            {/if}
          </span>
        </div>
      </ServiceKeyInformationSection>
    </div>
    {#if isNotCumulative || hasFundingLabels || isQpvOrZrr}
      <div class="gap-s12 text-f14 flex flex-col leading-16 font-bold">
        {#if isNotCumulative}
          <ServiceKeyInformationLabel
            icon={ErrorWarningFillSystem}
            label="Ce service n’est pas cumulable avec d’autres dispositifs"
            textClass="text-warning"
          />
        {/if}
        {#if hasFundingLabels}
          <ServiceKeyInformationLabel
            icon={MoneyEuroCircleFillFinance}
            label="Financé par&#8239;: {service.fundingLabelsDisplay.join(
              ', '
            )}"
            textClass="text-info"
          />
        {/if}
        {#if isQpvOrZrr}
          <ServiceKeyInformationLabel
            icon={InformationFillSystem}
            label="Uniquement QPV ou ZRR"
            textClass="text-info"
          />
        {/if}
      </div>
    {/if}
  </div>
</section>
