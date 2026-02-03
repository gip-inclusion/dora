<script lang="ts">
  import AddCircleFillSystem from "svelte-remix/AddCircleFillSystem.svelte";
  import ErrorWarningFillSystem from "svelte-remix/ErrorWarningFillSystem.svelte";
  import MoneyEuroCircleLineFinance from "svelte-remix/MoneyEuroCircleLineFinance.svelte";
  import InformationFillSystem from "svelte-remix/InformationFillSystem.svelte";
  import MapPinUserFillMap from "svelte-remix/MapPinUserFillMap.svelte";
  import TimeLineSystem from "svelte-remix/TimeLineSystem.svelte";

  import type { Service, ServicesOptions, ShortService } from "$lib/types";
  import { getLabelFromValue } from "$lib/utils/choice";
  import { shortenString } from "$lib/utils/misc";
  import { isNotFreeService } from "$lib/utils/service";

  import OsmHours from "../../osm-hours.svelte";

  interface Props {
    service: Service | ShortService;
    servicesOptions: ServicesOptions;
    display?: "sidebar" | "full";
  }

  let { service, servicesOptions, display = "full" }: Props = $props();

  let isDI = $derived("source" in service);
</script>

<h2 class:text-f23={display === "sidebar"}>Informations clés</h2>

<div class="gap-s12 flex flex-col">
  {#if service.isCumulative != null}
    {#if service.isCumulative}
      <div class="bold text-available flex items-center font-bold">
        <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
          <AddCircleFillSystem />
        </span>
        Ce service est cumulable avec d’autres dispositifs
      </div>
    {:else}
      <div class="bold text-error flex items-center font-bold">
        <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
          <ErrorWarningFillSystem />
        </span>
        Ce service n’est pas cumulable avec d’autres dispositifs
      </div>
    {/if}
  {/if}

  {#if service.feeCondition && isNotFreeService(service.feeCondition)}
    <div class="bold text-error flex items-center font-bold">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        <ErrorWarningFillSystem />
      </span>
      Frais à charge du bénéficiaire
    </div>
  {/if}

  {#if service.qpvOrZrr}
    <div class="bold text-info flex items-center font-bold">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        <InformationFillSystem />
      </span>
      Uniquement QPV ou ZRR
    </div>
  {/if}

  {#if display === "sidebar"}
    <hr class="mb-s10 mt-s20" />
  {/if}

  {#if service.feeCondition && isNotFreeService(service.feeCondition)}
    <div>
      <h3>
        <span class="mr-s8 h-s24 w-s24 fill-current">
          <MoneyEuroCircleLineFinance />
        </span>
        Frais à charge
      </h3>
      <p class="block">
        {getLabelFromValue(service.feeCondition, servicesOptions.feeConditions)}
      </p>
      <p class="block">
        {service.feeDetails != null
          ? service.feeDetails
          : "La structure n’a pas précisé le montant des frais"}
      </p>
    </div>
  {/if}

  {#if service.recurrence}
    <div>
      <h3>
        <span class="mr-s8 h-s24 w-s24 fill-current">
          <TimeLineSystem />
        </span>
        Fréquence et horaires
      </h3>
      <p>
        {#if isDI}
          <OsmHours osmHours={service.recurrence} />
        {:else}
          {service.recurrence}
        {/if}
      </p>
    </div>
  {/if}

  <div>
    <h3>
      <span class="mr-s8 h-s24 w-s24 fill-current">
        <MapPinUserFillMap />
      </span>
      Accueil
    </h3>
    {#if service.locationKinds?.length}
      <div class="gap-s6 flex flex-col">
        {#if service.locationKinds.includes("en-presentiel")}
          <p class="mb-s6">
            <strong>En présentiel&nbsp;•&nbsp;</strong>
            {service.address1}{#if service.address2}, {service.address2}{/if},
            {service.postalCode}&nbsp;{service.city}
          </p>
        {/if}

        {#if service.locationKinds.includes("a-distance")}
          <p>
            <strong>À distance</strong>
            {#if service.remoteUrl}
              <strong>&nbsp;•&nbsp;</strong>
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
      <p>Non renseigné</p>
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
</style>
