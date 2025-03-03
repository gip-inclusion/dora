<script lang="ts">
  import {
    addCircleIcon,
    errorWarningIcon,
    euroFillIcon,
    euroLineIcon,
    informationIcon,
    mapPinUserFillIcon,
    priceTagIcon,
    timeLineIcon,
    listCheckIcon,
    timerFlashIcon,
  } from "$lib/icons";
  import type { Service, ServicesOptions } from "$lib/types";
  import { getLabelFromValue } from "$lib/utils/choice";
  import { shortenString } from "$lib/utils/misc";
  import { isValidformatOsmHours } from "$lib/utils/opening-hours";
  import { isNotFreeService } from "$lib/utils/service";
  import OsmHours from "../../osm-hours.svelte";
  import ServiceDuration from "./service-duration.svelte";
  import SubcategoryList from "./subcategory-list.svelte";

  export let service: Service;
  export let servicesOptions: ServicesOptions;

  $: isDI = "source" in service;

  // trier les types dans l'ordre d'affichage du formulaire
  $: sortedServiceKindsDisplay = service.kindsDisplay?.sort((a, b) =>
    a.localeCompare(b)
  );
</script>

<h2 class="text-f23">Informations clés</h2>

<div class="gap-s12 flex flex-col">
  {#if service.fundingLabelsDisplay.length > 0}
    <div class="bold text-info flex items-center font-bold">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        {@html euroFillIcon}
      </span>
      Financé par&#8239;: {service.fundingLabelsDisplay.join(", ")}
    </div>
  {/if}
  {#if service.isCumulative != null}
    {#if service.isCumulative}
      <div class="bold text-available flex items-center font-bold">
        <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
          {@html addCircleIcon}
        </span>
        Ce service est cumulable avec d’autres dispositifs
      </div>
    {:else}
      <div class="bold text-warning flex items-center font-bold">
        <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
          {@html errorWarningIcon}
        </span>
        Ce service n’est pas cumulable avec d’autres dispositifs
      </div>
    {/if}
  {/if}
  {#if service.feeCondition && isNotFreeService(service.feeCondition)}
    <div class="bold text-warning flex items-center font-bold">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        {@html errorWarningIcon}
      </span>
      Frais à charge du bénéficiaire
    </div>
  {/if}

  {#if service.qpvOrZrr}
    <div class="bold text-info flex items-center font-bold">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        {@html informationIcon}
      </span>
      Uniquement QPV ou ZRR
    </div>
  {/if}

  <hr class="mb-s10 mt-s20" />

  <div>
    <h3 class="mb-s10!">
      <span class="mr-s8 h-s24 w-s24 fill-current">
        {@html listCheckIcon}
      </span>
      Les catégories de besoins
    </h3>
    <SubcategoryList {service} {servicesOptions} />
  </div>

  <hr class="mb-s10 mt-s20" />

  {#if service.durationWeeklyHours && service.durationWeeks}
    <div class="flex-1">
      <h3>
        <span class="mr-s8 h-s24 w-s24 shrink-0 self-baseline fill-current">
          {@html timerFlashIcon}
        </span>
        Durée de la prestation
      </h3>
      <ServiceDuration {service} />
    </div>
    <hr class="mb-s10 mt-s20" />
  {/if}

  <div class="flex">
    <div class="flex-1">
      <h3>
        <span class="mr-s8 h-s24 w-s24 shrink-0 self-baseline fill-current">
          {@html priceTagIcon}
        </span>
        Type de service
      </h3>

      <ul class="text-f16 text-gray-text inline-flex flex-wrap">
        {#if Array.isArray(service.kindsDisplay)}
          {#each sortedServiceKindsDisplay as kind, index (kind)}
            <li class:separator={index > 0}>{kind}</li>
          {/each}
        {:else}
          <li>Non renseigné</li>
        {/if}
      </ul>
    </div>

    {#if service.feeCondition && isNotFreeService(service.feeCondition)}
      <div class="flex-1">
        <h3>
          <span class="mr-s8 h-s24 w-s24 shrink-0 self-baseline fill-current">
            {@html euroLineIcon}
          </span>
          Frais à charge
        </h3>
        <p class="pb-s10 block">
          {getLabelFromValue(
            service.feeCondition,
            servicesOptions.feeConditions
          )}
        </p>
        <p class="block">
          {service.feeDetails != null
            ? service.feeDetails
            : "La structure n’a pas précisé le montant des frais"}
        </p>
      </div>
    {/if}
  </div>

  <hr class="mb-s10 mt-s20" />

  <div class="flex">
    <div class="flex-1">
      <h3>
        <span class="mr-s8 h-s24 w-s24 shrink-0 self-baseline fill-current">
          {@html mapPinUserFillIcon}
        </span>
        Lieu d’accueil
      </h3>
      {#if service.locationKinds?.length}
        <div class="gap-s6 flex flex-col">
          {#if service.locationKinds.includes("en-presentiel")}
            <p class="mb-s6">
              Présentiel,<br />
              {#if service.address1}
                {service.address1}{#if service.address2}, {service.address2}{/if},
              {/if}
              {service.postalCode}&nbsp;{service.city}
            </p>
          {/if}

          {#if service.locationKinds.includes("a-distance")}
            <p>
              À distance
              {#if service.remoteUrl}
                ,<br />
                <a
                  target="_blank"
                  rel="noopener ugc"
                  href={service.remoteUrl}
                  class="underline"
                  title="Ouverture dans une nouvelle fenêtre"
                >
                  {shortenString(service.remoteUrl, 35)}
                </a>
              {/if}
            </p>
          {/if}
        </div>
      {:else}
        <p class="mb-s6">Non renseigné</p>
      {/if}
    </div>

    {#if service.recurrence}
      <div class="flex-1">
        <h3>
          <span class="mr-s8 h-s24 w-s24 shrink-0 self-baseline fill-current">
            {@html timeLineIcon}
          </span>
          Fréquence et horaires
        </h3>
        <p>
          {#if isDI && isValidformatOsmHours(service.recurrence)}
            <OsmHours osmHours={service.recurrence} />
          {:else}
            {service.recurrence}
          {/if}
        </p>
      </div>
    {/if}
  </div>
</div>

<style lang="postcss">
  @reference "../../../../../app.css";

  h3 {
    @apply mb-s2 mt-s10 text-f17 flex items-center;
  }
  p {
    @apply m-s0 text-f16 text-gray-text;
  }
  li.separator::before {
    content: "•";
    @apply mx-s6;
  }
</style>
