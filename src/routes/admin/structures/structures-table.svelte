<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Tag from "$lib/components/display/tag.svelte";
  import { eyeIcon, phoneLineIcon } from "$lib/icons";
  import type { AdminShortStructure, ModerationStatus } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { capitalize, shortenString } from "$lib/utils/misc";
  import StructureModal from "./structure-modal.svelte";

  export let filteredStructures: AdminShortStructure[];
  export let selectedStructureSlug: string | null;
  export let onRefresh;

  let isStructureModalOpen = false;
  let currentStructure: AdminShortStructure | null = null;

  function getModerationStatusVerbose(status: ModerationStatus): string {
    switch (status) {
      case "NEED_INITIAL_MODERATION":
        return "Première modération nécessaire";
      case "NEED_NEW_MODERATION":
        return "Nouvelle modération nécessaire";
      case "IN_PROGRESS":
        return "Modération en cours";
      case "VALIDATED":
        return "Validé";
      default:
        return "";
    }
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
      on:mouseenter={() => (selectedStructureSlug = structure.slug)}
      on:mouseleave={() => (selectedStructureSlug = null)}
    >
      <div class="flex grow flex-row items-center">
        <div>
          <div>
            <strong
              ><a
                href="/structures/{structure.slug}"
                target="_blank"
                rel="noreferrer"
              >
                {shortenString(capitalize(structure.name))}
              </a>
            </strong>

            <div class="mt-s4 flex w-full flex-col gap-s4">
              {#if structure.moderationStatus !== "VALIDATED" || structure.numOutdatedServices}
                <div class="ap-s4 flex w-full">
                  {#if structure.moderationStatus !== "VALIDATED"}
                    <Tag bgColorClass="bg-error"
                      >{getModerationStatusVerbose(
                        structure.moderationStatus
                      )}</Tag
                    >
                  {/if}
                  {#if structure.numOutdatedServices}
                    <Tag bgColorClass="bg-warning">à mettre à jour</Tag>
                  {/if}
                </div>
              {/if}
              <div class="flex w-full  gap-s4">
                {#if !structure.hasAdmin}
                  <Tag bgColorClass="bg-magenta-cta">orpheline</Tag>
                {/if}

                {#if structure.numServices && !structure.numPublishedServices}
                  <Tag bgColorClass="bg-info">pas de services publiés</Tag>
                {/if}

                {#if !structure.numServices}
                  <Tag bgColorClass="bg-info">pas de services</Tag>
                {/if}
              </div>
              <!-- Suggestions: bg-success -->
            </div>
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
    </div>
  {/each}
</div>

<style lang="postcss">
  .highlight {
    @apply bg-gray-01 shadow-sm;
  }
</style>
