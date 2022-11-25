<script lang="ts">
  import Label from "$lib/components/label.svelte";
  import { mapPinIcon } from "$lib/icons";
  import { capitalize } from "$lib/utils";

  export let structure;
  export let showAddress = true;
</script>

<div class="flex flex-col rounded-md bg-white shadow-md">
  <div class="grow rounded-t-md bg-magenta-brand px-s20 py-s12">
    <h4 class="mb-s8 text-white">
      <a href="/structures/{structure.slug}">{capitalize(structure.name)}</a>
    </h4>

    {#if showAddress && (structure.postalCode || structure.city)}
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
