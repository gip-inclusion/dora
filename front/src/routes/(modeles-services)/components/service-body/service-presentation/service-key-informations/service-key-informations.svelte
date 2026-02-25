<script lang="ts">
  import CalendarTodoFillBusiness from "svelte-remix/CalendarTodoFillBusiness.svelte";
  import CheckboxCircleFillSystem from "svelte-remix/CheckboxCircleFillSystem.svelte";
  import Compass3FillMap from "svelte-remix/Compass3FillMap.svelte";
  import ErrorWarningFillSystem from "svelte-remix/ErrorWarningFillSystem.svelte";
  import GroupFillUserFaces from "svelte-remix/GroupFillUserFaces.svelte";
  import MapPin2FillMap from "svelte-remix/MapPin2FillMap.svelte";
  import MoneyEuroCircleFillFinance from "svelte-remix/MoneyEuroCircleFillFinance.svelte";
  import TimeFillSystem from "svelte-remix/TimeFillSystem.svelte";

  import OsmHours from "$lib/components/specialized/osm-hours.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getLabelFromValue } from "$lib/utils/choice";
  import { shortenString } from "$lib/utils/misc";
  import { isNotFreeService, isDurationValid } from "$lib/utils/service";
  import { isService } from "$lib/utils/typeguards";

  import ServiceFeedbackButton from "../../../../services/[slug]/service-feedback-button.svelte";
  import ServiceDuration from "./service-duration.svelte";
  import ServiceKeyInformationLabel from "./service-key-information-label.svelte";
  import ServiceKeyInformationSection from "./service-key-information-section.svelte";

  interface Props {
    service: Service | Model;
    servicesOptions: ServicesOptions;
    onFeedbackButtonClick?: () => void;
  }

  let { service, servicesOptions, onFeedbackButtonClick }: Props = $props();
  let isDI = $derived("source" in service);

  let isNotCumulative = $derived(!service.isCumulative);
  let hasFundingLabels = $derived(service.fundingLabelsDisplay.length > 0);
  let hasLabelSection = $derived(isNotCumulative || hasFundingLabels);

  let eligibilityRequirements = $derived([
    ...(service.accessConditionsDisplay || []),
    ...(service.requirementsDisplay || []),
    ...(service.qpvOrZrr ? ["Uniquement QPV ou ZRR"] : []),
  ]);

  let addressForMapLink = $derived(
    isService(service)
      ? `${service.address1} ${service.postalCode} - ${service.city}`
      : null
  );
  let mapLink = $derived(
    addressForMapLink
      ? `https://nominatim.openstreetmap.org/ui/search.html?q=${encodeURIComponent(addressForMapLink)}`
      : null
  );
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
          {#each service.publicsDisplay || [] as pub}
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
        title="Les critères d’admission"
      >
        {#if eligibilityRequirements.length === 1}
          <!-- Les services DI n'ont qu'un seul élément de critère d'admission mais il peut comporter plusieurs lignes.
               On affiche chaque ligne comme élément de liste. -->
          <ul class="list-inside list-disc">
            {#each eligibilityRequirements[0].split("\n") as requirement (requirement)}
              <li>{requirement}</li>
            {/each}
          </ul>
        {:else if eligibilityRequirements.length > 1}
          <ul class="list-inside list-disc">
            {#each eligibilityRequirements as requirement (requirement)}
              <li>{requirement}</li>
            {/each}
          </ul>
        {:else if isDI}
          Aucun détail n’a été renseigné par la structure
        {:else}
          Aucun critère d’admission spécifique
        {/if}
      </ServiceKeyInformationSection>
    </div>
    {#if !service.isModel || service.recurrence}
      <div class="pb-s32 gap-s32 flex flex-col sm:flex-row sm:flex-wrap">
        {#if !service.isModel}
          <ServiceKeyInformationSection
            icon={MapPin2FillMap}
            title="Lieu d’accueil"
          >
            {#if service.locationKinds && service.locationKinds.length > 0}
              <div class="gap-s12 flex flex-col">
                {#if service.locationKinds.includes("en-presentiel")}
                  <div class="flex flex-col">
                    <strong>Présentiel</strong>
                    {#if service.addressLine}
                      <address class="not-italic">
                        {service.addressLine}
                      </address>
                      {#if mapLink}
                        <a
                          class="text-magenta-cta mt-s4 font-bold"
                          href={mapLink}
                          target="_blank"
                          rel="noopener ugc">Voir sur la carte</a
                        >
                      {/if}
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
        {/if}
        {#if service.recurrence}
          <ServiceKeyInformationSection
            icon={TimeFillSystem}
            title="Fréquence et horaires"
          >
            {#if isDI}
              <OsmHours osmHours={service.recurrence} />
            {:else}
              {service.recurrence}
            {/if}
          </ServiceKeyInformationSection>
        {/if}
        {#if !service.isModel}
          <ServiceKeyInformationSection
            icon={Compass3FillMap}
            title="Périmètre géographique"
          >
            {service.diffusionZoneDetailsDisplay}
          </ServiceKeyInformationSection>
        {/if}
      </div>
    {/if}
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
    <div class:pb-s32={hasLabelSection}>
      <ServiceKeyInformationSection
        icon={MoneyEuroCircleFillFinance}
        title="Frais à charge"
      >
        <div class="flex flex-col">
          {#if service.feeCondition}
            <span
              class={isNotFreeService(service.feeCondition)
                ? "text-warning font-bold"
                : "font-bold"}
            >
              {getLabelFromValue(
                service.feeCondition,
                servicesOptions.feeConditions
              )}
            </span>
          {/if}
          {#if service.feeCondition && isNotFreeService(service.feeCondition)}
            <span>
              {#if service.feeDetails}
                {service.feeDetails}
              {:else}
                Aucun détail n’a été renseigné par la structure
              {/if}
            </span>
          {/if}
        </div>
      </ServiceKeyInformationSection>
      {#if !hasLabelSection && onFeedbackButtonClick}
        <div class="mt-s32">
          <ServiceFeedbackButton onclick={onFeedbackButtonClick} />
        </div>
      {/if}
    </div>
    {#if hasLabelSection}
      <div>
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
        </div>
        {#if onFeedbackButtonClick}
          <div class="mt-s32">
            <ServiceFeedbackButton onclick={onFeedbackButtonClick} />
          </div>
        {/if}
      </div>
    {/if}
  </div>
</section>
