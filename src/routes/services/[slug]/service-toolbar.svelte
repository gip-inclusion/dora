<script lang="ts">
  import cornerLeftBlueImg from "$lib/assets/style/corner-left-blue.png";
  import cornerRightBlueImg from "$lib/assets/style/corner-right-blue.png";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import ServiceStateUpdateSelect from "$lib/components/specialized/services/service-state-update-select.svelte";
  import SynchronizedIcon from "$lib/components/specialized/services/synchronized-icon.svelte";
  import { copyIcon2 } from "$lib/icons";
  import type { Service, ServicesOptions } from "$lib/types";
  import { token } from "$lib/utils/auth";
  import {
    computeUpdateStatusData,
    computeUpdateStatusLabel,
  } from "$lib/utils/service";
  import ServiceUpdateStatusAsContributor from "./service-update-status-as-contributor.svelte";
  import ServiceUpdateStatusAsReader from "./service-update-status-as-reader.svelte";

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
      service.status === 'PUBLISHED' &&
      updateStatusData.updateStatus === 'NEEDED'
        ? 'bg-service-orange'
        : ''}

        {service.canWrite &&
      service.status === 'PUBLISHED' &&
      updateStatusData.updateStatus === 'REQUIRED'
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

  {#if !service.canWrite || updateStatusData.updateStatus === "NOT_NEEDED" || service.status !== "PUBLISHED"}
    <div
      class="m-auto max-w-6xl border border-t-0 border-r-0 border-l-0 border-gray-02"
    />
  {/if}

  {#if updateStatusData.updateStatus === "NOT_NEEDED" || !$token}
    <img
      src={cornerLeftBlueImg}
      alt=""
      class="absolute -top-[1px] left-s0 print:hidden"
    />
    <img
      src={cornerRightBlueImg}
      alt=""
      class="absolute -top-[1px] right-s0 print:hidden"
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
          {:else if !service.useInclusionNumeriqueScheme}
            <LinkButton
              label="Utiliser comme modèle"
              icon={copyIcon2}
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
