<script lang="ts">
  import Label from "$lib/components/display/label.svelte";
  import { pageLineIcon } from "$lib/icons";
  import { capitalize } from "$lib/utils/misc";
  import type { Structure } from "$lib/types";

  interface Props {
    structure: Structure;
    showAddress?: boolean;
  }

  let { structure, showAddress = true }: Props = $props();
</script>

<div class="flex flex-col rounded-lg bg-white shadow-md">
  <div class="bg-magenta-brand p-s24 grow rounded-t-md">
    <h3 class="mb-s12 text-f19 min-h-[100px] text-white">
      <a href="/structures/{structure.slug}">{capitalize(structure.name)}</a>
    </h3>

    {#if showAddress && (structure.postalCode || structure.city)}
      <Label label={`${structure.city} (${structure.postalCode})`} />
    {/if}
  </div>
  <div class="px-s20 py-s16">
    <div class="mb-s0 text-f14 text-gray-dark flex items-center">
      <div
        class="mr-s8 h-s28 w-s28 bg-service-blue text-service-blue-dark flex items-center justify-center rounded-full"
      >
        <span class="h-s16 w-s16 inline-block fill-current">
          {@html pageLineIcon}
        </span>
      </div>

      {structure.numServices} service{structure.numServices > 1 ? "s" : ""}
    </div>
  </div>
</div>
