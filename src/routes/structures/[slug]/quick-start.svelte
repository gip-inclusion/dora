<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import {
    checkboxCircleFillIcon,
    checkboxBlankCircle,
    closeIcon,
  } from "$lib/icons";
  import {
    isStructureInformationsComplete,
    hasAtLeastOneServiceNotArchived,
    hasAtLeastTwoMembersOrInvitedMembers,
  } from "./quick-start";
  import type {
    Structure,
    StructureMember,
    PutativeStructureMember,
  } from "$lib/types";
  import { modifyStructure } from "$lib/requests/structures";

  export let structure: Structure;
  export let members: StructureMember[];
  export let putativeMembers: PutativeStructureMember[];

  async function hideQuickStart() {
    await modifyStructure({ slug: structure.slug, quickStartDone: true });
    structure.quickStartDone = true;
  }

  $: steps = [
    {
      label: "Compléter le profil de votre structure",
      complete: isStructureInformationsComplete(structure),
      url: `/structures/${structure.slug}/editer`,
    },
    {
      label: "Inviter vos collaborateurs",
      complete: hasAtLeastTwoMembersOrInvitedMembers(members, putativeMembers),
      url: `/structures/${structure.slug}/collaborateurs`,
    },
    {
      label: "Référencer un premier service",
      complete: hasAtLeastOneServiceNotArchived(structure),
      url: `/services/creer?structure=${structure.slug}`,
    },
  ];

  $: if (
    steps.filter(({ complete }) => complete).length === steps.length &&
    !structure.quickStartDone
  ) {
    hideQuickStart();
  }
</script>

{#if !structure.quickStartDone}
  <div class="rounded-md border border-gray-03">
    <div
      class="relative flex items-center justify-between gap-s16 border-b border-gray-01 px-s16 pb-s24 pt-s24 sm:flex-row sm:px-s36"
    >
      <div>
        <h2 class="mb-s0 text-f23">Guide de démarrage rapide</h2>
        <p class="m-s0 text-f14">Vos premiers pas sur DORA</p>
      </div>

      <button class="flex" on:click={hideQuickStart}>
        <span class="h-s24 w-s24 fill-magenta-cta">
          {@html closeIcon}
        </span>
        <span class="sr-only">Masquer le guide</span>
      </button>
    </div>

    <div class="px-s16 font-bold sm:px-s36">
      <ul>
        {#each steps as { label, complete, url }}
          <li
            class:line-through={complete}
            class="flex items-center border-b border-gray-01 py-s16 sm:py-s36"
          >
            <a
              class="flex hover:underline"
              href={url}
              class:fill-success={complete}
            >
              <span class="mr-s16 h-s24 w-s24">
                {@html complete ? checkboxCircleFillIcon : checkboxBlankCircle}
              </span>
              {label}
            </a>
          </li>
        {/each}

        <li class="py-s36 text-right">
          <Button
            label="Masquer le guide"
            secondary
            on:click={hideQuickStart}
          />
        </li>
      </ul>
    </div>
  </div>
{/if}
