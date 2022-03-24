<script>
  import { mapPinIcon } from "$lib/icons";
  import Label from "$lib/components/label.svelte";

  export let structure;
</script>

<div class="rounded-md shadow-md">
  <div class="rounded-t-md bg-magenta-brand px-s20 py-s12">
    <h4 class="mb-s8 text-white">
      <a href="/structures/{structure.slug}">{structure.name}</a>
    </h4>

    {#if structure.postalCode || structure.city}
      <Label
        label={`${structure.postalCode}, ${structure.city}`}
        smallIcon
        darkBg
        icon={mapPinIcon}
      />
    {/if}
  </div>
  <div class="py-s16 px-s20">
    <p class="mb-s0 text-f14">
      {structure.numServices} service{structure.numServices > 1 ? "s" : ""}
    </p>
  </div>
</div>
