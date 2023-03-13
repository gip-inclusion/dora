<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import {
    checkboxCircleFillIcon,
    checkboxBlankCircle,
    closeIcon,
  } from "$lib/icons";
  import {
    canShowQuickStart,
    isStructureInformationsComplete,
    isFirstSearchDone,
    hasOneService,
    hasAtLeastTwoMembers,
    saveQuickStartDone,
  } from "./quick-start";
  import type { Structure, StructureMember } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";

  export let structure: Structure;
  export let members: StructureMember[];

  let showQuickStart = canShowQuickStart(structure);

  function hideQuickStart() {
    saveQuickStartDone(structure.slug);
    showQuickStart = false;
  }

  $: steps = [
    {
      label: "Compléter le profil de votre structure",
      complete: isStructureInformationsComplete(structure),
      url: `/structures/${structure.slug}/editer`,
    },
    {
      label: "Inviter vos collaborateurs",
      complete: hasAtLeastTwoMembers(members),
      url: `/structures/${structure.slug}/collaborateurs`,
    },
    {
      label: "Référencer un de vos services",
      complete: hasOneService(structure),
      url: `/services/creer?structure=${structure.slug}`,
    },
    {
      label: "Faire votre première recherche",
      complete: isFirstSearchDone($userInfo),
      url: "/",
    },
  ];

  $: canCloseQuickStart = steps.filter(({ complete }) => complete).length >= 2;
  $: if (steps.filter(({ complete }) => complete).length === steps.length) {
    hideQuickStart();
  }
</script>

{#if showQuickStart}
  <div class="rounded-md border border-gray-03">
    <div
      class="relative flex items-center justify-between gap-s16 border-b border-gray-01 px-s16 pb-s24 pt-s24 sm:flex-row sm:px-s35"
    >
      <div>
        <h2 class="mb-s0 text-f23">Guide de démarrage rapide</h2>
        <p class="m-s0 text-f14">Vos premiers pas sur DORA</p>
      </div>

      {#if canCloseQuickStart}
        <button class="flex" on:click={hideQuickStart}>
          <span class="h-s24 w-s24 fill-magenta-cta">
            {@html closeIcon}
          </span>
          <span class="sr-only">Masquer le guide</span>
        </button>
      {/if}
    </div>

    <div class="px-s16 font-bold sm:px-s35">
      <ul>
        {#each steps as { label, complete, url }}
          <li
            class:line-through={complete}
            class="flex items-center border-b border-gray-01 py-s16 sm:py-s35"
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

        <li class="py-s35 text-right">
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
