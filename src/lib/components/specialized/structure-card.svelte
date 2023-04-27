<script lang="ts">
  import Label from "$lib/components/display/label.svelte";
  import { pageLineIcon } from "$lib/icons";
  import { capitalize } from "$lib/utils/misc";

  export let structure;
  export let showAddress = true;
</script>

<div class="flex flex-col rounded-md bg-white shadow-md">
  <div class="grow rounded-t-md bg-magenta-brand p-s24">
    <h3 class="mb-s12 min-h-[100px] text-f19 text-white">
      <a href="/structures/{structure.slug}">{capitalize(structure.name)}</a>
    </h3>

    {#if showAddress && (structure.postalCode || structure.city)}
      <Label label={`${structure.city} (${structure.postalCode})`} darkBg />
    {/if}
  </div>
  <div class="py-s16 px-s20">
    <div class="mb-s0 flex items-center text-f14 text-gray-dark">
      <div
        class="mr-s8 flex h-s28 w-s28 items-center justify-center rounded-full bg-service-blue text-service-blue-dark"
      >
        <span class="inline-block h-s16 w-s16 fill-current">
          {@html pageLineIcon}
        </span>
      </div>

      {structure.numServices} service{structure.numServices > 1 ? "s" : ""}
    </div>
  </div>
</div>
