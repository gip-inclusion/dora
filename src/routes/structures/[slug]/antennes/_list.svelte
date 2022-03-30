<script>
  import { API_URL, CANONICAL_URL } from "$lib/env";
  import { userInfo } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import StructureCard from "$lib/components/structures/card.svelte";
  import { addCircleIcon } from "$lib/icons";
  export let structure, branches, total;
  export let hasListLink = false;

  $: structureFrontEndLink = `${CANONICAL_URL}/structures/${encodeURIComponent(
    structure.slug
  )}/collaborateurs`;
  $: structureBackEndLink = `${API_URL}/admin/structures/structure/?q=${encodeURIComponent(
    structure.slug
  )}`;
</script>

<div class="col-span-full md:flex md:items-center md:justify-between">
  <h2 class="mb-s24 text-france-blue">Antennes</h2>
  <div class="flex gap-s16">
    {#if !!branches.length && hasListLink}
      <LinkButton
        label={`Voir toutes les antennes (${total})`}
        to="/structures/{structure.slug}/antennes"
        small
        secondary
      />
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
    {#each branches as branch}
      <StructureCard structure={branch} />
    {/each}
  </div>
</div>
