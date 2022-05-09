<script>
  import { homeIcon, eyeIcon } from "$lib/icons";
  import { shortenString } from "$lib/utils";

  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import ButtonMenu from "$lib/components/services/button-menu.svelte";
  import ServiceStateLabel from "$lib/components/services/state-label.svelte";

  export let service;
  export let showStructure;
  export let readOnly;
  export let onRefresh;
</script>

<div class="flex flex-row items-center gap-s16 rounded-md bg-white p-s16">
  <div class="flex-auto basis-1/3">
    <a href="/services/{service.slug}">
      <h5 class="mb-s0">{shortenString(service.name)}</h5>
    </a>

    {#if showStructure}
      <Label
        label={`${service.structureInfo.name}`}
        smallIcon
        icon={homeIcon}
      />
    {/if}
  </div>
  <div class="flex flex-none basis-1/6 flex-col">
    {#if service.diffusionZoneType !== "country"}
      <Label label={service.diffusionZoneTypeDisplay} />
    {/if}
    <Label label={service.diffusionZoneDetailsDisplay} bold />
  </div>
  <div class="flex-none basis-s112">
    <ServiceStateLabel {service} />
  </div>
  <div class="flex-none basis-s40">
    <Label
      label={`${new Date(service.modificationDate).toLocaleDateString(
        "fr",
        "short"
      )}`}
    />
  </div>
  <div class="flex-none basis-s32">
    <LinkButton to="/services/{service.slug}" icon={eyeIcon} noBackground />
  </div>
  {#if !readOnly}
    <div class="flex-none basis-s32">
      <ButtonMenu {service} {onRefresh} />
    </div>
  {/if}
</div>
