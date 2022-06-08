<script>
  import { checkBoxBlankIcon } from "$lib/icons";
  import Label from "$lib/components/label.svelte";
  import ServiceButtonMenu from "./service-button-menu.svelte";
  import StateButtonMenu from "./state-button-menu.svelte";
  export let service;
  export let readOnly = true;
  export let onRefresh;
</script>

<div class="flex flex-col justify-between rounded-md bg-white shadow-md">
  <div
    class="flex grow flex-col justify-between rounded-t-md bg-gray-00 px-s20 py-s12"
    class:rounded-b-md={readOnly}
  >
    <div>
      <div class="mb-s8 flex items-center">
        {#if !service.isDraft && !service.isSuggestion}
          <div class="mr-s8">
            <Label icon={checkBoxBlankIcon} success bold smallIcon />
          </div>
        {/if}
        <p class="mb-s0 text-f12 text-gray-text">
          Mis à jour le {new Date(service.modificationDate).toLocaleDateString(
            "fr-FR",
            {
              year: "numeric",
              month: "long",
              day: "numeric",
            }
          )}
        </p>
      </div>
      <h4 class="mb-s8 text-france-blue">
        <a href="/services/{service.slug}">{service.name}</a>
      </h4>
    </div>
    {#if service.diffusionZoneDetailsDisplay}
      <Label label={service.diffusionZoneDetailsDisplay} />
    {/if}
  </div>
  {#if !readOnly}
    <div
      class="flex items-center justify-between border-t  border-t-gray-03 p-s20"
    >
      <StateButtonMenu {service} {onRefresh} />

      {#if !service.isSuggestion}
        <ServiceButtonMenu {service} />
      {/if}
    </div>
  {/if}
</div>
