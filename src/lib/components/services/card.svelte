<script>
  import Tag from "$lib/components/tag.svelte";
  import { mapPinIcon } from "$lib/icons";
  import Label from "$lib/components/label.svelte";
  import StateLabel from "./state-label.svelte";
  import Menu from "./menu.svelte";
  export let service;
  export let readOnly = true;
  export let onRefresh;
</script>

<div class="rounded-md px-s20 py-s12 shadow-md">
  <div class="flex items-center justify-between">
    <StateLabel {service} />
    {#if !readOnly}
      <Menu {service} {onRefresh} />
    {/if}
  </div>
  <hr class="mt-s8 border-t border-gray-03 " />
  <div class="my-s8 flex flex-col gap-s16">
    <h4><a href="/services/{service.slug}">{service.name}</a></h4>

    <Tag selfStart>{service.categoryDisplay}</Tag>
    {#if service.postalCode || service.city}
      <Label
        label={`${service.postalCode}, ${service.city}`}
        smallIcon
        icon={mapPinIcon}
      />
    {/if}
  </div>
</div>
