<script lang="ts">
  import {
    SERVICE_STATUSES,
    SERVICE_UPDATE_STATUS,
    type Service,
    type ServicesOptions,
  } from "$lib/types";
  import { token } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";

  import cornerLeftBlueImg from "$lib/assets/corner-left-blue.png";
  import cornerRightBlueImg from "$lib/assets/corner-right-blue.png";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import SynchronizedIcon from "$lib/components/services/icons/synchronized.svelte";

  import ServiceUpdateStatusAsContributor from "./service-update-status-as-contributor.svelte";
  import ServiceUpdateStatusAsReader from "./service-update-status-as-reader.svelte";
  import ServiceStateUpdateSelect from "../../service-state-update-select.svelte";
  import {
    computeUpdateStatusData,
    computeUpdateStatusLabel,
  } from "$lib/utils/service";
  import { copyIcon } from "$lib/icons";

  export let service: Service;
  export let servicesOptions: ServicesOptions;
  export let onRefresh: () => void;

  $: updateStatusData = computeUpdateStatusData(service);
  $: label = computeUpdateStatusLabel(updateStatusData);
</script>

<div id="service-update-status" class="relative">
  <div class={updateStatusData.updateStatus}>
    <CenteredGrid
      extraClass="
        py-s32 mb-s14 w-full
        {service.canWrite &&
      service.status === SERVICE_STATUSES.PUBLISHED &&
      updateStatusData.updateStatus === SERVICE_UPDATE_STATUS.NEEDED
        ? 'bg-service-orange'
        : ''}

        {service.canWrite &&
      service.status === SERVICE_STATUSES.PUBLISHED &&
      updateStatusData.updateStatus === SERVICE_UPDATE_STATUS.REQUIRED
        ? 'bg-service-red'
        : ''}
      "
      noPadding
    >
      {#if service.canWrite}
        <ServiceUpdateStatusAsContributor
          monthDiff={updateStatusData.monthDiff}
          {label}
          {onRefresh}
          updateStatus={updateStatusData.updateStatus}
          {service}
          {servicesOptions}
        />
      {:else}
        <ServiceUpdateStatusAsReader
          {label}
          monthDiff={updateStatusData.monthDiff}
          updateStatus={updateStatusData.updateStatus}
          {service}
        />
      {/if}
    </CenteredGrid>
  </div>

  {#if !service.canWrite || updateStatusData.updateStatus === SERVICE_UPDATE_STATUS.NOT_NEEDED || service.status !== SERVICE_STATUSES.PUBLISHED}
    <div
      class="m-auto max-w-6xl border border-t-0 border-r-0 border-l-0 border-gray-02"
    />
  {/if}

  {#if updateStatusData.updateStatus === SERVICE_UPDATE_STATUS.NOT_NEEDED || !$token}
    <img
      src={cornerLeftBlueImg}
      alt=""
      class="noprint absolute -top-[1px] left-s0"
    />
    <img
      src={cornerRightBlueImg}
      alt=""
      class="noprint absolute -top-[1px] right-s0"
    />
  {/if}

  {#if service.canWrite}
    <CenteredGrid extraClass="w-full" noPadding>
      <div
        class="flex w-full flex-col place-content-between items-center gap-s24 py-s32 sm:flex-row"
      >
        <div>
          <ServiceStateUpdateSelect
            {service}
            {servicesOptions}
            {onRefresh}
            hideLabel={false}
          />
        </div>
        <div class="flex h-s48 items-center md:self-end">
          {#if service.model}
            {#if service.modelChanged}
              <div class="flex items-center text-f14 font-bold text-gray-text">
                <span class="mr-s10"><SynchronizedIcon warning /></span>
                <a href="/services/{service.slug}/editer" class="underline">
                  Mise à jour du modèle disponible
                </a>
              </div>
            {:else}
              <div class="flex items-center text-f14 italic text-gray-text">
                <span class="mr-s10"><SynchronizedIcon /></span>
                <a href="/modeles/{service.model}" class="underline">
                  Synchronisé avec un modèle
                </a>
              </div>
            {/if}
          {:else}
            <LinkButton
              label="Utiliser comme modèle"
              icon={copyIcon}
              iconOnRight
              noBackground
              hoverUnderline
              to={`/modeles/creer?service=${service.slug}&structure=${service.structure}`}
            />
          {/if}
        </div>
      </div>
    </CenteredGrid>
  {/if}
</div>

<style lang="postcss">
  .NOT_NEEDED {
    @apply mx-auto flex items-center;
  }
  .NEEDED {
    @apply bg-service-orange;
  }
  .REQUIRED {
    @apply bg-service-red;
  }
</style>
