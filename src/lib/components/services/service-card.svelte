<script>
  import { checkBoxBlankIcon } from "$lib/icons";
  import Label from "$lib/components/label.svelte";
  import ServiceButtonMenu from "./service-button-menu.svelte";
  import StateButtonMenu from "./state-button-menu.svelte";
  import Date from "../date.svelte";
  import ServiceSync from "./service-sync.svelte";
  import { SERVICE_STATUSES } from "$lib/schemas/service";
  export let service;
  export let readOnly = true;
  export let onRefresh;
</script>

<div class="flex flex-col justify-between rounded-md bg-white shadow-md">
  <div
    class="grow rounded-t-md bg-gray-00 px-s20 py-s12"
    class:rounded-b-md={readOnly}
  >
    <p class="mb-s8 text-f14 text-gray-text">
      Mis à jour le <Date date={service.modificationDate} />
    </p>

    <h4 class="mb-s8 text-france-blue">
      <a href="/services/{service.slug}">{service.name}</a>
    </h4>

    <div class="mb-s8 flex items-center">
      {#if service.status === SERVICE_STATUSES.published}
        <div class="mr-s8">
          <Label icon={checkBoxBlankIcon} success bold smallIcon />
        </div>
      {/if}
      {#if service.diffusionZoneDetailsDisplay}
        <Label label={service.diffusionZoneDetailsDisplay} />
      {/if}
    </div>
  </div>
  {#if !readOnly}
    <div class="flex flex-col justify-end border-t border-t-gray-03 p-s20">
      <div class="mb-s24">
        {#if service.model}
          <ServiceSync modelChanged={service.modelChanged} border={false} />
        {:else}
          <div class="flex text-f14">
            <span>&nbsp;</span>
          </div>
        {/if}
      </div>
      <div class="flex items-center justify-between">
        <StateButtonMenu {service} {onRefresh} />

        {#if service.status !== SERVICE_STATUSES.suggestion && service.status !== SERVICE_STATUSES.archived}
          <ServiceButtonMenu {service} />
        {/if}
      </div>
    </div>
  {/if}
</div>
