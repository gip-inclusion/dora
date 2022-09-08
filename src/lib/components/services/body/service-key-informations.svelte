<script lang="ts">
  import {
    addCircleIcon,
    errorWarningIcon,
    euroLineIcon,
    timeLineIcon,
    mapPinUserFillIcon,
    informationIcon,
  } from "$lib/icons";

  import type { DashboardService, Service } from "$lib/types";
  import { shortenString } from "$lib/utils";

  export let service: Service | DashboardService;
  export let display: "sidebar" | "full" = "full";
</script>

<h2 class:text-f23={display === "sidebar"}>Informations clés</h2>

<div class="flex flex-col gap-s12">
  {#if service.isCumulative}
    <div class="bold flex items-center font-bold text-available">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        {@html addCircleIcon}
      </span>
      Ce service est cumulable avec d’autres dispositifs
    </div>
  {:else}
    <div class="bold flex items-center font-bold text-error">
      <span class="mr-s8 h-s24 w-s24 min-w-[24px] fill-current">
        {@html errorWarningIcon}
      </span>
      Ce service n'est pas cumulable avec d’autres dispositifs
    </div>
  {/if}

  {#if service.hasFee}
    <div class="bold flex items-center font-bold text-error">
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
      Uniquement QPV + ZRR
    </div>
  {/if}

  {#if display === "sidebar"}
    <hr class="mt-s20 mb-s10" />
  {/if}

  {#if service.hasFee}
    <div>
      <h3>
        <span class="mr-s8 h-s24 w-s24 fill-current">
          {@html euroLineIcon}
        </span>
        Frais à charge
      </h3>
      <p>{service.feeDetails}</p>
    </div>
  {/if}

  {#if service.recurrence}
    <div>
      <h3>
        <span class="mr-s8 h-s24 w-s24 fill-current">
          {@html timeLineIcon}
        </span>
        Fréquence et horaires
      </h3>
      <p>{service.recurrence}</p>
    </div>
  {/if}

  {#if service.locationKinds.length}
    <div>
      <h3>
        <span class="mr-s8 h-s24 w-s24 fill-current">
          {@html mapPinUserFillIcon}
        </span>
        Accueil
      </h3>

      <div class="flex flex-col gap-s6">
        {#if service.locationKinds.includes("en-presentiel")}
          <p class="mb-s6">
            <strong>En présentiel&nbsp;•&nbsp;</strong>
            {service.address1}{#if service.address2}{service.address2}{/if},
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
                rel="noopener nofollow"
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
</div>

<style lang="postcss">
  h3 {
    @apply mt-s10 mb-s2 flex items-center text-f17;
  }
  p {
    @apply m-s0 text-f16 text-gray-text;
  }
</style>
