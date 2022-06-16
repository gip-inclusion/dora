<script>
  import { checkBoxBlankIcon } from "$lib/icons";
  import Label from "$lib/components/label.svelte";
  import ServiceButtonMenu from "./service-button-menu.svelte";
  import StateButtonMenu from "./state-button-menu.svelte";
  import Date from "../date.svelte";
  import ServiceSync from "./service-sync.svelte";
  export let service;
  export let readOnly = true;
  export let onRefresh;
</script>

<div class="flex flex-col justify-between rounded-md bg-white shadow-md">
  <div
    class="rounded-t-md bg-gray-00 px-s20 py-s12"
    class:rounded-b-md={readOnly}
  >
    <p class="mb-s8 text-f14 text-gray-text">
      Mis à jour le <Date date={service.modificationDate} />
    </p>

    <h4 class="mb-s8 text-france-blue">
      <a href="/services/{service.slug}">{service.name}</a>
    </h4>

    <div class="mb-s8 flex items-center">
      {#if !service.isDraft && !service.isSuggestion}
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
    <div class="flex grow flex-col justify-end border-t border-t-gray-03 p-s20">
      {#if service.model}
        <div class="mb-s24">
          <ServiceSync modelChanged={service.modelChanged} border={false} />
        </div>
      {/if}
      <div class="flex items-center justify-between">
        <StateButtonMenu {service} {onRefresh} />

        {#if !service.isSuggestion}
          <ServiceButtonMenu {service} />
        {/if}
      </div>
    </div>
  {/if}
</div>
