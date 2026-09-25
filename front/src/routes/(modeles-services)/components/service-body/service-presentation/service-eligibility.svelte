<script lang="ts">
  import CheckboxCircleFillSystem from "svelte-remix/CheckboxCircleFillSystem.svelte";
  import CompassDiscoverFillMap from "svelte-remix/CompassDiscoverFillMap.svelte";
  import GroupFillUserFaces from "svelte-remix/GroupFillUserFaces.svelte";
  import MoneyEuroCircleFillFinance from "svelte-remix/MoneyEuroCircleFillFinance.svelte";
  import SendPlane2FillBusiness from "svelte-remix/SendPlane2FillBusiness.svelte";
  import File2FillDocument from "svelte-remix/File2FillDocument.svelte";

  import ExternalLinkIcon from "$lib/components/display/external-link-icon.svelte";
  import TextClamp from "$lib/components/display/text-clamp.svelte";
  import ServiceList from "./components/service-list.svelte";

  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getLabelFromValue } from "$lib/utils/choice";
  import { isNotFreeService } from "$lib/utils/service";
  import { formatFilePath } from "$lib/utils/file";

  import ServiceKeyInformationSection from "./service-key-informations/service-key-information-section.svelte";
  import { NATIONAL_ELIGIBLITITY_ZONE } from "$lib/consts";

  interface Props {
    service: Service | Model;
    servicesOptions: ServicesOptions;
  }

  let { service, servicesOptions }: Props = $props();

  const eligibilityZones = service.zoneEligibiliteDisplay
    ?.map((zone) => zone.label)
    .join(" · ");

  const accessConditions = service.conditionsAcces
    ? service.conditionsAcces
        .split("\n")
        .map((condition) => condition.trim())
        .filter(Boolean)
        .map((condition) => `- ${condition}`)
        .join("\n")
    : "";

  let hasDocuments = $derived(
    (Array.isArray(service.formsInfo) && service.formsInfo.length > 0) ||
      service.onlineForm
  );
</script>

<section>
  <h2 class="text-f23 text-france-blue mb-s16 leading-32 font-bold">
    Éligibilité au service
  </h2>

  <div
    class="border-gray-02 p-s32 gap-s32 divide-gray-01 text-f16 text-gray-text [&_p]:mb-s0 [&_p]:text-f16 flex flex-col divide-y rounded-2xl border leading-24 [&_p]:leading-24"
  >
    <div class="pb-s32">
      <ServiceKeyInformationSection
        icon={GroupFillUserFaces}
        title="Le public concerné"
      >
        <ul
          class="[&>li+li]:before:mx-s6 [&>li]:inline [&>li+li]:before:inline [&>li+li]:before:content-['·']"
        >
          {#if service.publicsDisplay === null}
            <li>Non renseigné</li>
          {:else}
            {#each service.publicsDisplay as pub}
              <li>{pub}</li>
            {:else}
              <li>Tous publics</li>
            {/each}
          {/if}
        </ul>
        {#if service.publicsPrecisions}
          <div class="mt-s16 whitespace-pre-line">
            {service.publicsPrecisions}
          </div>
        {/if}
      </ServiceKeyInformationSection>
    </div>
    <div class="pb-s32">
      <ServiceKeyInformationSection
        icon={CheckboxCircleFillSystem}
        title="Les conditions d’accès"
      >
        {#if accessConditions}
          <div
            class="[&_ul]:pl-s0 [&_ul]:my-s0 [&_ul]:space-y-s2 [&_li]:my-s0 [&_li]:pl-s0 [&_li]:text-f16 [&_.prose]:max-w-none [&_li]:leading-24 [&_li]:marker:text-current [&_ul]:list-inside [&_ul]:list-disc"
          >
            <TextClamp text={accessConditions} />
          </div>
        {:else}
          <div>Non renseigné</div>
        {/if}
      </ServiceKeyInformationSection>
    </div>
    {#if hasDocuments}
      <div class="pb-s32">
        <ServiceKeyInformationSection
          icon={File2FillDocument}
          title="Documents à compléter"
        >
          <ServiceList>
            {#if Array.isArray(service.formsInfo)}
              {#each service.formsInfo as form}
                <li>
                  <a
                    class="underline"
                    target="_blank"
                    href={form.url}
                    title="Ouverture dans une nouvelle fenêtre"
                    rel="noopener ugc">{formatFilePath(form.name)}</a
                  >
                </li>
              {/each}
            {/if}
            {#if service.onlineForm}
              <li>
                <a
                  class="underline"
                  target="_blank"
                  href={service.onlineForm}
                  title="Ouverture dans une nouvelle fenêtre"
                  rel="noopenernoreferrer ugc"
                  >{service.onlineForm}<ExternalLinkIcon /></a
                >
              </li>
            {/if}
          </ServiceList>
        </ServiceKeyInformationSection>
      </div>
    {/if}
    <div class="pb-s32">
      <ServiceKeyInformationSection
        icon={MoneyEuroCircleFillFinance}
        title="Frais à charge"
      >
        <div class="gap-s4 flex flex-col">
          {#if service.feeCondition}
            <span
              class={isNotFreeService(service.feeCondition)
                ? "text-warning font-bold"
                : "text-available font-bold"}
            >
              {getLabelFromValue(
                service.feeCondition,
                servicesOptions.feeConditions
              )}
            </span>
          {/if}
          {#if service.feeCondition}
            <span>
              {#if isNotFreeService(service.feeCondition)}
                {#if service.feeDetails}
                  {service.feeDetails}
                {:else}
                  Aucun détail n’a été renseigné par la structure
                {/if}
              {/if}
            </span>
          {/if}
        </div>
      </ServiceKeyInformationSection>
    </div>
    <div class="pb-s32">
      <ServiceKeyInformationSection
        icon={SendPlane2FillBusiness}
        title="Méthode d’orientation"
      >
        <div class="gap-s16 flex flex-col">
          {#if service.mobilisableByDisplay}
            <div>
              <h4 class="text-f16 text-gray-dark mb-s4 leading-24 font-bold">
                Service mobilisable par
              </h4>
              {service.mobilisableByDisplay.join(" et ")}
            </div>
          {/if}
          {#if service.mobilisationModesDisplay}
            <div>
              <h4 class="text-f16 text-gray-dark mb-s4 leading-24 font-bold">
                Modes de mobilisation
              </h4>
              {service.mobilisationModesDisplay.join(" · ")}
            </div>
          {/if}
          {#if service.mobilisationDetails}
            <div class="whitespace-pre-line">
              {service.mobilisationDetails}
            </div>
          {/if}
        </div>
      </ServiceKeyInformationSection>
    </div>
    <div>
      <ServiceKeyInformationSection
        icon={CompassDiscoverFillMap}
        title="Zone d’éligibilité"
      >
        {#if eligibilityZones}
          <TextClamp text={eligibilityZones} />
        {:else}
          <span>{NATIONAL_ELIGIBLITITY_ZONE}</span>
        {/if}
      </ServiceKeyInformationSection>
    </div>
  </div>
</section>
