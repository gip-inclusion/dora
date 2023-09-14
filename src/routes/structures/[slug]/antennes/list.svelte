<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Button from "$lib/components/display/button.svelte";
  import StructureCard from "$lib/components/specialized/structure-card.svelte";
  import { API_URL, CANONICAL_URL } from "$lib/env";
  import { home3Icon } from "$lib/icons";
  import Count from "../count.svelte";
  import NewBranchModal from "./new-branch-modal.svelte";

  export let structure, branches, total;
  export let tabDisplay = true;
  export let limit;

  let newBranchModalOpen = false;

  let departements = [];
  // let departement = "tous";
  const departement = "tous";
  let filters;
  let branchesFiltered = [];

  function branchesFilter(allBranches) {
    let filteredBranches = allBranches.filter(
      (b) =>
        (departement === "tous" || b.department === departement) &&
        (!filters ||
          filters
            .split(" ")
            .every((filter) =>
              b.name.toLowerCase().includes(filter.toLowerCase())
            ))
    );

    if (limit) {
      filteredBranches = filteredBranches.slice(0, limit);
    }

    return filteredBranches;
  }

  $: structureFrontEndLink = `${CANONICAL_URL}/structures/${encodeURIComponent(
    structure.slug
  )}/collaborateurs`;
  $: structureBackEndLink = `${API_URL}/admin/structures/structure/?q=${encodeURIComponent(
    structure.slug
  )}`;
  $: departements = branches.reduce(
    (depts, branch) => {
      if (!depts.map((dept) => dept.value).includes(branch.department)) {
        depts.push({ value: branch.department, label: branch.department });
      }

      return depts;
    },
    [{ value: "tous", label: "Tous" }]
  );
  $: branchesFiltered = branchesFilter(branches);
</script>

<div class="mb-s24 md:flex md:items-center md:justify-between">
  <div class="flex flex-row gap-s8">
    <h2 class="mb-s0 text-france-blue">Antennes</h2>
    {#if limit}<Count>{total}</Count>{/if}
  </div>
  <div class="flex gap-s16">
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
        on:click={() => (newBranchModalOpen = true)}
        icon={home3Icon}
      />
    {/if}

    <!-- {#if hasOptions}
      <div class="flex flex-col gap-s16 md:flex-row md:items-center">
        <div>Départements</div>
        <div>
          <Select
            choices={departements}
            bind:value={departement}
            initialValue={departement}
            on:blur
            showClear={false}
          />
        </div>

        <Input type="text" bind:value={filters} placeholder="Mots-clé" />
      </div>
    {/if} -->
  </div>
</div>

<div class="mb-s48 grid gap-s16 md:grid-cols-2 lg:grid-cols-3">
  {#each branchesFiltered as branch}
    <StructureCard structure={branch} />
  {/each}
</div>

<NewBranchModal
  bind:isOpen={newBranchModalOpen}
  on:close={() => (newBranchModalOpen = false)}
/>
