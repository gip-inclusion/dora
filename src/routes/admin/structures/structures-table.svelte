<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Tag from "$lib/components/display/tag.svelte";
  import { eyeIcon, phoneLineIcon } from "$lib/icons";
  import type {
    AdminShortStructure,
    ModerationStatus,
    ServicesOptions,
  } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { capitalize, shortenString } from "$lib/utils/misc";
  import StructureModale from "./structure-modale.svelte";

  export let servicesOptions: ServicesOptions;
  export let filteredStructures: AdminShortStructure[];
  export let selectedStructureSlug: string | null;

  let isStructureModalOpen = false;
  let currentStructure: AdminShortStructure;

  function getModerationStatusVerbose(status: ModerationStatus): string {
    switch (status) {
      case "NEED_INITIAL_MODERATION":
        return "Première modération nécessaire";
      case "NEED_NEW_MODERATION":
        return "Nouvelle modération nécessaire";
      case "IN_PROGRESS":
        return "En cours";
      case "VALIDATED":
        return "Validé";
      default:
        return "";
    }
  }
</script>

{#if currentStructure}
  <StructureModale
    bind:isOpen={isStructureModalOpen}
    structureSlug={currentStructure?.slug}
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

            {#if structure.typologyDisplay}<div class="text-f12 italic">
                ({shortenString(structure.typologyDisplay)})
              </div>{/if}

            <div class="my-s4 flex w-full flex-wrap gap-s4">
              {#each structure.categories.slice(0, 3) as cat}
                <Tag bgColorClass="bg-magenta-brand"
                  ><div class="whitespace-nowrap">
                    {servicesOptions.categories.find(
                      (option) => option.value === cat
                    )?.label}
                  </div></Tag
                >
              {/each}
              {#if structure.categories.length > 3}
                <Tag bgColorClass="bg-magenta-brand">…</Tag>
              {/if}
            </div>

            <div class="flex w-full flex-wrap gap-s4 ">
              {#if !structure.hasAdmin}
                <Tag bgColorClass="bg-error">orpheline</Tag>
              {/if}

              {#if structure.numOutdatedServices}
                <Tag bgColorClass="bg-warning">à mettre à jour</Tag>
              {/if}

              {#if !structure.numPublishedServices}
                <Tag bgColorClass="bg-warning">pas de services</Tag>
              {/if}
              {#if structure.moderationStatus !== "VALIDATED"}
                <Tag bgColorClass="bg-warning"
                  >{getModerationStatusVerbose(structure.moderationStatus)}</Tag
                >
              {/if}
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
