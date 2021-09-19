<script context="module">
  import { getStructure } from "$lib/structures";

  export async function load({ page, _fetch, _session, _context }) {
    return {
      props: { structure: await getStructure(page.params.slug) },
    };
  }
</script>

<script>
  import insane from "insane";

  import { page } from "$app/stores";
  import { token } from "$lib/auth";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  export let structure;

  const editLink = `${$page.path}/edit`;
</script>

<svelte:head>
  <title>Dora: {structure.name}</title>
</svelte:head>

<CenteredGrid roundedbg>
  <div class="col-span-8 col-start-1 mb-4 text-gray-text">
    <h3>{structure.name}</h3>
    <div class="flex flex-col gap-1">
      <div class="text-sm text-gray-text-alt">
        <span class="font-bold">SIRET :</span>
        {structure.siret}
      </div>
      <div>
        <span class="font-bold">Type : </span>{structure.typologyDisplay}
      </div>

      <div><span class="font-bold">Description courte :</span></div>
      <div class="ml-2">{structure.shortDesc}</div>
      <div>
        <span class="font-bold">Département :</span>
        {structure.postalCode.slice(0, 2)}
      </div>

      <div><span class="font-bold">Adresse :</span></div>
      <div class="ml-2">
        <div>{structure.address1}</div>
        {#if structure.address2}
          <div>{structure.address2}</div>
        {/if}
        <div>{structure.postalCode} {structure.city}</div>
      </div>
      <div><span class="font-bold">Téléphone :</span> {structure.phone}</div>
      {#if structure.email}
        <div>
          <span class="font-bold">Email :</span>
          <a class="underline" href="mailto:{structure.email}">
            {structure.email}
          </a>
        </div>
      {/if}
      {#if structure.url}
        <div>
          <span class="font-bold">Site :</span>
          <a
            class="underline"
            target="_blank"
            rel="noopener nofollow"
            href={structure.url}>
            {structure.url}
          </a>
        </div>
      {/if}

      <div><span class="font-bold">Description détaillée :</span></div>
      <div class="prose-sm bg-gray-01 ml-2 pl-1 border-l border-gray-03 mb-4">
        {@html insane(structure.fullDesc)}
      </div>
    </div>
    {#if $token}
      <LinkButton to={editLink} label="Éditer" />
    {/if}
  </div>
</CenteredGrid>
