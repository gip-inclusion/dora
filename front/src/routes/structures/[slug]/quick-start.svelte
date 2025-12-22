<script lang="ts">
  import CheckboxCircleFillSystem from "svelte-remix/CheckboxCircleFillSystem.svelte";
  import CheckboxBlankCircleLineSystem from "svelte-remix/CheckboxBlankCircleLineSystem.svelte";
  import CloseFillSystem from "svelte-remix/CloseFillSystem.svelte";

  import Button from "$lib/components/display/button.svelte";
  import { modifyStructure } from "$lib/requests/structures";
  import type {
    Structure,
    StructureMember,
    PutativeStructureMember,
  } from "$lib/types";

  import {
    isStructureInformationsComplete,
    hasAtLeastOneServiceNotArchived,
    hasAtLeastTwoMembersOrInvitedMembers,
  } from "./quick-start";

  interface Props {
    structure: Structure;
    members: StructureMember[];
    putativeMembers: PutativeStructureMember[];
  }

  let { structure = $bindable(), members, putativeMembers }: Props = $props();

  async function hideQuickStart() {
    await modifyStructure({ slug: structure.slug, quickStartDone: true });
    structure.quickStartDone = true;
  }

  let steps = $derived([
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
  ]);

  $effect(() => {
    if (
      steps.filter(({ complete }) => complete).length === steps.length &&
      !structure.quickStartDone
    ) {
      hideQuickStart();
    }
  });
</script>

{#if !structure.quickStartDone}
  <div class="border-gray-03 rounded-lg border">
    <div
      class="gap-s16 border-gray-01 px-s16 pb-s24 pt-s24 sm:px-s36 relative flex items-center justify-between border-b sm:flex-row"
    >
      <div>
        <h2 class="mb-s0 text-f23">Guide de démarrage rapide</h2>
        <p class="m-s0 text-f14">Vos premiers pas sur DORA</p>
      </div>

      <button class="flex" onclick={hideQuickStart}>
        <span class="h-s24 w-s24 fill-magenta-cta">
          <CloseFillSystem />
        </span>
        <span class="sr-only">Masquer le guide</span>
      </button>
    </div>

    <div class="px-s16 sm:px-s36 font-bold">
      <ul>
        {#each steps as { label, complete, url }}
          <li
            class:line-through={complete}
            class="border-gray-01 py-s16 sm:py-s36 flex items-center border-b"
          >
            <a
              class="flex hover:underline"
              href={url}
              class:fill-success={complete}
            >
              <span class="mr-s16 h-s24 w-s24">
                {#if complete}
                  <CheckboxCircleFillSystem />
                {:else}
                  <CheckboxBlankCircleLineSystem />
                {/if}
              </span>
              {label}
            </a>
          </li>
        {/each}

        <li class="py-s36 text-right">
          <Button label="Masquer le guide" secondary onclick={hideQuickStart} />
        </li>
      </ul>
    </div>
  </div>
{/if}
