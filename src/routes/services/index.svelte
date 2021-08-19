<script context="module">
  import { getServices } from "$lib/services";

  export async function load({ _page, _fetch, _session, _context }) {
    return getServices();
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  export let services = [];

  function shortenString(str, length = 40) {
    if (str.length > length) {
      return `${str.slice(0, length)}…`;
    }
    return str;
  }
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
        {#each services as service}
          <tr>
            <td>
              <LinkButton
                label={shortenString(service.name)}
                to={`/services/${service.slug}`}
                noBackground />
            </td>
            <td>xxx</td>
            <td> xxx </td>
            <td>xx</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</CenteredGrid>
