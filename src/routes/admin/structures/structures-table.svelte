<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { eyeIcon, phoneLineIcon } from "$lib/icons";
  import { modifyStructure } from "$lib/requests/structures";
  import type { AdminShortStructure } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { capitalize, shortenString } from "$lib/utils/misc";
  import StructureModal from "./structure-modal.svelte";

  export let filteredStructures: AdminShortStructure[];
  export let selectedStructureSlug: string | null;
  export let onRefresh;

  let isStructureModalOpen = false;
  let currentStructure: AdminShortStructure | null = null;

  async function updateStructureObsolete(
    structure: AdminShortStructure,
    isObsolete: boolean
  ) {
    structure.isObsolete = isObsolete;
    await modifyStructure({ slug: structure.slug, isObsolete });
    onRefresh();
  }
</script>

{#if currentStructure}
  <StructureModal
    bind:isOpen={isStructureModalOpen}
    structureSlug={currentStructure?.slug}
    {onRefresh}
  />
{/if}

<div class="flex flex-col gap-s8">
  {#each filteredStructures as structure}
    <div
      class="flex flex-row gap-s16 rounded-md border border-gray-01 p-s16 shadow-xs"
      class:highlight={selectedStructureSlug === structure.slug}
      role="presentation"
      on:mouseenter={() => (selectedStructureSlug = structure.slug)}
      on:mouseleave={() => (selectedStructureSlug = null)}
    >
      <div class="flex grow flex-row items-center">
        <div>
          <div>
            <strong
              ><a href="/structures/{structure.slug}" target="_blank">
                {shortenString(capitalize(structure.name))}
              </a>
            </strong>
          </div>
        </div>
      </div>

      {#if $userInfo.isStaff}
        <LinkButton
          to="/admin/structures/{structure.slug}"
          icon={eyeIcon}
          noBackground
          otherTab
        />
      {/if}
      <Button
        on:click={() => {
          currentStructure = structure;
          isStructureModalOpen = true;
        }}
        icon={phoneLineIcon}
        noBackground
      />
      {#if !structure.isObsolete}
        <Button
          small
          extraClass="font-normal !text-f12 w-[75px]"
          on:click={() => updateStructureObsolete(structure, true)}
          label="Rendre obsolète"
          secondary
        />
      {:else}
        <Button
          small
          extraClass="font-normal !text-f12 w-[75px]"
          on:click={() => updateStructureObsolete(structure, false)}
          label="Ré-activer"
          secondary
        />
      {/if}
    </div>
  {/each}
</div>

<style lang="postcss">
  .highlight {
    @apply bg-gray-01 shadow-sm;
  }
</style>
