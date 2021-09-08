<script context="module">
  import { getStructures } from "$lib/structures";

  export async function load({ _page, _fetch, _session, _context }) {
    return {
      props: {
        structures: await getStructures(),
      },
    };
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import { shortenString } from "$lib/utils";

  export let structures;
</script>

<style lang="postcss">
  td {
    @apply p-0 text-sm text-gray-text-alt;
  }
</style>

<CenteredGrid>
  <div class="col-start-1 col-span-full">
    <table class="table-auto p-6">
      <thead>
        <tr>
          <th>Nom</th><th>Dept</th><th>Typologie</th><th>SIRET</th>
        </tr>
      </thead>
      <tbody>
        {#each structures as structure}
          <tr>
            <td>
              <LinkButton
                label={shortenString(structure.name)}
                to={`/structures/${structure.slug}`}
                noBackground />
            </td>
            <td>{structure.department}</td>
            <td>
              {shortenString(structure.typologyDisplay)}
            </td>
            <td>{structure.siret}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</CenteredGrid>
