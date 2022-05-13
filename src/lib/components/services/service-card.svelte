<script>
  import { checkBoxBlankIcon, mapPinIcon } from "$lib/icons";
  import Label from "$lib/components/label.svelte";
  import ButtonMenu from "./button-menu.svelte";
  import StateButtonMenu from "./state-button-menu.svelte";
  export let service;
  export let readOnly = true;
  export let onRefresh;
</script>

<div class="flex flex-col justify-between rounded-md bg-white shadow-md">
  <div
    class="flex grow flex-col justify-between rounded-t-md bg-france-blue px-s20 py-s12"
    class:rounded-b-md={readOnly}
  >
    <div>
      <div class="mb-s8 flex items-center">
        {#if !service.isDraft && !service.isSuggestion}
          <Label
            label="Disponible"
            icon={checkBoxBlankIcon}
            success
            darkBg
            bold
            smallIcon
          />
          <p class="mx-s12 mb-s0 text-f12 text-gray-03">|</p>
        {/if}
        <p class="mb-s0 text-f12 text-gray-01">
          {new Date(service.modificationDate).toLocaleDateString("fr-FR", {
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
        </p>
      </div>
      <h4 class="mb-s8 text-white">
        <a href="/services/{service.slug}">{service.name}</a>
      </h4>
    </div>
    {#if service.diffusionZoneDetailsDisplay}
      <div>
        <Label
          label={service.diffusionZoneDetailsDisplay}
          icon={mapPinIcon}
          darkBg
          smallIcon
        />
      </div>
    {/if}
  </div>
  {#if !readOnly}
    <div class="flex items-center justify-between p-s20">
      <StateButtonMenu {service} {onRefresh} />

      {#if !service.isSuggestion}
        <ButtonMenu {service} {onRefresh} />
      {/if}
    </div>
  {/if}
</div>
