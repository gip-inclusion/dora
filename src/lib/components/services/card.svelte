<script>
  import { mapPinIcon } from "$lib/icons";
  import Label from "$lib/components/label.svelte";
  import StateLabel from "./state-label.svelte";
  import ButtonMenu from "./button-menu.svelte";
  export let service;
  export let readOnly = true;
  export let onRefresh;
</script>

<div class="rounded-md px-s20 py-s12 shadow-md">
  {#if !readOnly}
    <div class="flex items-center justify-between">
      <StateLabel {service} />

      <ButtonMenu {service} {onRefresh} />
    </div>
    <hr class="mt-s8 mb-s20 border-t border-gray-03 " />
  {/if}
  <div class="my-s8 flex flex-col gap-s16">
    <h4><a href="/services/{service.slug}">{service.name}</a></h4>

    {#if service.diffusionZoneDetailsDisplay}
      <Label
        label={`${service.diffusionZoneDetailsDisplay}`}
        smallIcon
        icon={mapPinIcon}
      />
    {/if}

    <p class="text-f14">
      Mis à jour le {new Date(service.modificationDate).toLocaleDateString(
        "fr",
        "short"
      )}
    </p>
  </div>
</div>
