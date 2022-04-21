<script>
  import { API_URL, CANONICAL_URL } from "$lib/env";
  import { userInfo } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import StructureCard from "$lib/components/structures/card.svelte";
  import { addCircleIcon } from "$lib/icons";
  import Select from "$lib/components/forms/select.svelte";
  import Input from "$lib/components/forms/input.svelte";
  export let structure, branches, total;
  export let hasOptions = true;

  let departements = [];
  let departement = "tous";
  let filters;
  let branchesFiltered = [];

  $: structureFrontEndLink = `${CANONICAL_URL}/structures/${encodeURIComponent(
    structure.slug
  )}/collaborateurs`;
  $: structureBackEndLink = `${API_URL}/admin/structures/structure/?q=${encodeURIComponent(
    structure.slug
  )}`;
  $: departements = branches.reduce(
    (acc, b) => {
      if (!acc.map((d) => d.value).includes(b.department)) {
        acc.push({ value: b.department, label: b.department });
      }

      return acc;
    },
    [{ value: "tous", label: "Tous" }]
  );
  $: branchesFiltered = branches.filter(
    (b) =>
      (departement === "tous" || b.department === departement) &&
      (!filters ||
        filters
          .split(" ")
          .every((f) => b.name.toLowerCase().includes(f.toLowerCase())))
  );
</script>

<div class="col-span-full md:flex md:items-center md:justify-between">
  <h2 class="mb-s24 text-france-blue">Antennes</h2>
  <div class="flex gap-s16">
    {#if !!branches.length && !hasOptions}
      <LinkButton
        label={`Voir toutes les antennes (${total})`}
        to="/structures/{structure.slug}/antennes"
        small
        secondary
      />
    {/if}

    {#if hasOptions}
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
    {/if}
  </div>
</div>
<div class="col-span-full">
  <div class="mb-s48 grid gap-s16 md:grid-cols-2 lg:grid-cols-4">
    {#if structure.isAdmin || $userInfo?.isStaff}
      <div
        class="flex items-center justify-center rounded-md px-s20 py-s24 shadow-md"
      >
        <LinkButton
          label="Ajouter une antenne…"
          to={`https://itou.typeform.com/to/IXADRw7j#courriel_demandeur=${encodeURIComponent(
            $userInfo.email
          )}&lien_frontend=${encodeURIComponent(
            structureFrontEndLink
          )}&lien_backend=${encodeURIComponent(structureBackEndLink)}`}
          icon={addCircleIcon}
          noBackground
          otherTab
          nofollow
        />
      </div>
    {/if}
    {#each branchesFiltered as branch}
      <StructureCard structure={branch} />
    {/each}
  </div>
</div>
