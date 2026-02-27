<script lang="ts">
  import Home3LineBuildings from "svelte-remix/Home3LineBuildings.svelte";

  import LinkButton from "$lib/components/display/link-button.svelte";
  import Button from "$lib/components/display/button.svelte";
  import StructureCard from "$lib/components/specialized/structure-card.svelte";

  import Count from "../count.svelte";
  import NewBranchModal from "./new-branch-modal.svelte";

  interface Props {
    structure: any;
    branches: any;
    total: any;
    tabDisplay?: boolean;
    limit: any;
  }

  let {
    structure,
    branches,
    total,
    tabDisplay = true,
    limit,
  }: Props = $props();

  let newBranchModalOpen = $state(false);
</script>

<div class="mb-s24 md:flex md:items-center md:justify-between">
  <div class="gap-s8 flex flex-row">
    <h2 class="mb-s0 text-france-blue">Antennes</h2>
    {#if limit}<Count>{total}</Count>{/if}
  </div>
  <div class="gap-s16 flex">
    {#if !!branches.length && !tabDisplay}
      <LinkButton
        label="Voir toutes les antennes"
        to="/structures/{structure.slug}/antennes"
        small
        noBackground
      />
    {/if}
    {#if structure.canEditInformations}
      <Button
        label="Ajouter une antenne"
        onclick={() => (newBranchModalOpen = true)}
        icon={Home3LineBuildings}
      />
    {/if}
  </div>
</div>

<div class="mb-s48 gap-s16 grid md:grid-cols-2 lg:grid-cols-3">
  {#each branches as branch}
    <StructureCard structure={branch} />
  {/each}
</div>

<NewBranchModal bind:isOpen={newBranchModalOpen} />
