<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { eyeIcon, moreIcon, phoneLineIcon } from "$lib/icons";
  import { modifyStructure } from "$lib/requests/structures";
  import type { AdminShortStructure } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { capitalize, shortenString } from "$lib/utils/misc";
  import StructureModal from "./structure-modal.svelte";

  interface Props {
    filteredStructures: AdminShortStructure[];
    selectedStructureSlug: string | null;
    onRefresh: any;
  }

  let {
    filteredStructures,
    selectedStructureSlug = $bindable(),
    onRefresh,
  }: Props = $props();

  let isStructureModalOpen = $state(false);
  let currentStructure: AdminShortStructure | null = $state(null);

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

<div class="gap-s8 flex flex-col">
  {#each filteredStructures as structure}
    <div
      class="gap-s16 border-gray-01 p-s16 flex flex-row items-center rounded-lg border shadow-xs"
      class:highlight={selectedStructureSlug === structure.slug}
      role="presentation"
      onmouseenter={() => (selectedStructureSlug = structure.slug)}
      onmouseleave={() => (selectedStructureSlug = null)}
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

      <ButtonMenu
        icon={moreIcon}
        small
        hideLabel
        label="Actions disponibles sur la structure"
      >
        {#snippet children({ onClose: onCloseParent })}
          {#if !structure.isObsolete}
            <Button
              on:click={() => {
                updateStructureObsolete(structure, true);
                onCloseParent();
              }}
              label="Rendre&nbsp;obsolète"
              small
              noBackground
            />
          {:else}
            <Button
              on:click={() => {
                updateStructureObsolete(structure, false);
                onCloseParent();
              }}
              label="Ré&#8209;activer"
              small
              noBackground
            />
          {/if}
        {/snippet}
      </ButtonMenu>
    </div>
  {/each}
</div>

<style lang="postcss">
  @reference "../../../app.css";

  .highlight {
    @apply bg-gray-01 shadow-sm;
  }
</style>
