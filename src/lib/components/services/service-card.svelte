<script lang="ts">
  import ServiceButtonMenu from "./service-button-menu.svelte";
  import ServiceStateUpdateSelect from "./service-state-update-select.svelte";
  import ServiceAvailability from "./body/service-availability.svelte";
  import {
    SERVICE_STATUSES,
    SERVICE_UPDATE_STATUS,
    type DashboardService,
  } from "$lib/types";
  import {
    computeUpdateStatusData,
    computeUpdateStatusLabel,
  } from "$lib/utils/service";

  import UpdateStatusIcon from "$lib/components/services/icons/update-status.svelte";
  import SynchronizedIcon from "$lib/components/services/icons/synchronized.svelte";

  export let service: DashboardService;
  export let servicesOptions;
  export let readOnly = true;
  export let onRefresh: () => void;

  $: updateStatusData = computeUpdateStatusData(service);
</script>

<div
  class="relative flex flex-col justify-between rounded-md bg-white shadow-md"
>
  <div class="g row mb-s32 rounded-t-md p-s24">
    <div class="mb-s24 flex items-center justify-between">
      <div class="relative z-10">
        <ServiceStateUpdateSelect
          {service}
          {servicesOptions}
          {onRefresh}
          fullWidth
        />
      </div>

      {#if service.status !== SERVICE_STATUSES.SUGGESTION && service.status !== SERVICE_STATUSES.ARCHIVED}
        <div class="relative z-10">
          <ServiceButtonMenu
            {service}
            {servicesOptions}
            {onRefresh}
            updateStatus={updateStatusData.updateStatus}
          />
        </div>
      {/if}
    </div>

    <h3 class="mb-s24 text-france-blue">
      <a class="full-card-link hover:underline" href="/services/{service.slug}"
        >{service.name}</a
      >
    </h3>

    <div class="mb-s8 flex items-center">
      <ServiceAvailability {service} small dark bold />
    </div>

    {#if service.diffusionZoneDetailsDisplay}
      <div class="mb-s8 flex items-center text-france-blue">
        Périmètre&nbsp;:&nbsp;<strong
          >{service.diffusionZoneDetailsDisplay}</strong
        >
      </div>
    {/if}
  </div>

  <div
    class="flex min-h-[100px] flex-col justify-center gap-s10 border-t border-t-gray-03 py-s12 px-s20"
  >
    <div class="flex items-center text-f14 text-gray-text">
      {#if updateStatusData.updateStatus === SERVICE_UPDATE_STATUS.NOT_NEEDED}
        <span class="mr-s8">
          <UpdateStatusIcon
            updateStatus={SERVICE_UPDATE_STATUS.NOT_NEEDED}
            small
          />
        </span>
        {computeUpdateStatusLabel(updateStatusData)}
      {:else if updateStatusData.updateStatus === SERVICE_UPDATE_STATUS.NEEDED}
        <span class="mr-s8">
          <UpdateStatusIcon updateStatus={SERVICE_UPDATE_STATUS.NEEDED} small />
        </span>
        <span class="font-bold">Actualisation conseillée</span>
      {:else if updateStatusData.updateStatus === SERVICE_UPDATE_STATUS.REQUIRED}
        <span class="mr-s8">
          <UpdateStatusIcon
            updateStatus={SERVICE_UPDATE_STATUS.REQUIRED}
            small
          />
        </span>
        <span class="font-bold">Actualisation requise</span>
      {/if}
    </div>

    {#if !readOnly && service.model}
      <div class="flex items-center text-f14">
        {#if service.modelChanged}
          <span class="mr-s8"><SynchronizedIcon warning small /></span>
          <a
            href="/services/{service.slug}/editer"
            class="relative hover:underline"
          >
            <span class="font-bold">Mise à jour disponible</span>
          </a>
        {:else}
          <span class="mr-s8"><SynchronizedIcon small /></span>
          <span class="italic text-gray-text">
            Synchronisé avec un modèle
          </span>
        {/if}
      </div>
    {/if}
  </div>
</div>

<style lang="postcss">
  /*
  * Link is on <h2> but we want all the card clickable (in an accessible way)
  * Source: http://inclusive-components.design/cards/
  */
  .full-card-link::after {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
  }
</style>
