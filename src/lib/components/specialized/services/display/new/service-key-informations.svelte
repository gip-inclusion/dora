<script lang="ts">
  import {
    addCircleIcon,
    errorWarningIcon,
    euroLineIcon,
    informationIcon,
    mapPinUserFillIcon,
    priceTagIcon,
    timeLineIcon,
    listCheckIcon,
  } from "$lib/icons";
  import type { Service, ServicesOptions } from "$lib/types";
  import { getLabelFromValue } from "$lib/utils/choice";
  import { shortenString } from "$lib/utils/misc";
  import { isNotFreeService } from "$lib/utils/service";
  import SubcategoryList from "./subcategory-list.svelte";

  export let service: Service;
  export let servicesOptions: ServicesOptions;
</script>

<h2 class="text-f23">Informations clés</h2>

<div class="flex flex-col gap-s12">
  {#if service.isCumulative}
    <div class="bold flex items-center font-bold text-available">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        {@html addCircleIcon}
      </span>
      Ce service est cumulable avec d’autres dispositifs
    </div>
  {:else}
    <div class="bold flex items-center font-bold text-warning">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        {@html errorWarningIcon}
      </span>
      Ce service n'est pas cumulable avec d’autres dispositifs
    </div>
  {/if}

  {#if service.feeCondition && isNotFreeService(service.feeCondition)}
    <div class="bold flex items-center font-bold text-warning">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        {@html errorWarningIcon}
      </span>
      Frais à charge du bénéficiaire
    </div>
  {/if}

  {#if service.qpvOrZrr}
    <div class="bold flex items-center font-bold text-info">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        {@html informationIcon}
      </span>
      Uniquement QPV ou ZRR
    </div>
  {/if}

  <hr class="mt-s20 mb-s10" />

  <div>
    <h3 class="!mb-s10 text-f17">
      <span class="mr-s8 h-s24 w-s24 fill-current">
        {@html listCheckIcon}
      </span>
      Les catégories de besoins
    </h3>
    <SubcategoryList {service} {servicesOptions} />
  </div>

  <hr class="mt-s20 mb-s10" />

  <div class="flex">
    <div class="flex-1">
      <h3>
        <span class="mr-s8 h-s24 w-s24 fill-current">
          {@html priceTagIcon}
        </span>
        Type de service
      </h3>

      <ul class="inline-flex flex-wrap text-f16 text-gray-text">
        {#each service.kindsDisplay as kind, index (kind)}
          <li class:separator={index > 0}>{kind}</li>
        {/each}
      </ul>
    </div>

    {#if service.feeCondition && isNotFreeService(service.feeCondition)}
      <div class="flex-1">
        <h3>
          <span class="mr-s8 h-s24 w-s24 fill-current">
            {@html euroLineIcon}
          </span>
          Frais à charge
        </h3>
        <p class="block pb-s10">
          {getLabelFromValue(
            service.feeCondition,
            servicesOptions.feeConditions
          )}
        </p>
        <p class="block">{service.feeDetails}</p>
      </div>
    {/if}
  </div>

  <hr class="mt-s20 mb-s10" />

  <div class="flex w-full gap-s32">
    {#if service.locationKinds?.length}
      <div class="flex-1">
        <h3>
          <span class="mr-s8 h-s24 w-s24 fill-current">
            {@html mapPinUserFillIcon}
          </span>
          Lieu d'accueil
        </h3>

        <div class="flex flex-col gap-s6">
          {#if service.locationKinds.includes("en-presentiel")}
            <p class="mb-s6">
              Présentiel,<br />
              {service.address1}{#if service.address2}{service.address2}{/if},
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
      </div>
    {/if}

    {#if service.recurrence}
      <div class="flex-1">
        <h3>
          <span class="mr-s8 h-s24 w-s24 fill-current">
            {@html timeLineIcon}
          </span>
          Fréquence et horaires
        </h3>
        <p>{service.recurrence}</p>
      </div>
    {/if}
  </div>
</div>

<style lang="postcss">
  h3 {
    @apply mt-s10 mb-s2 flex items-center text-f17;
  }
  p {
    @apply m-s0 text-f16 text-gray-text;
  }
  li.separator::before {
    content: "•";
    @apply mx-s6;
  }
</style>
