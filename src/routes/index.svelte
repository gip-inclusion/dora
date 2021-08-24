<script context="module">
  import { getPublicServicesOptions } from "$lib/services";

  export async function load({ _page, _fetch, _session, _context }) {
    return getPublicServicesOptions();
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  import SearchForm from "./_homepage/_search-form.svelte";

  export let servicesOptions;
</script>

<CenteredGrid>
  <div class="col-start-1 col-span-full mb-5">
    <SearchForm {servicesOptions} />
    <!-- <LinkButton label="Design System" to="design-system" noBackground /> -->
    <LinkButton label="Voir les structures" to="/structures" noBackground />
    <LinkButton
      label="Créer une structure"
      to="/structures/creer"
      noBackground />
    <LinkButton label="Voir les services" to="/services" noBackground />
    <LinkButton label="Créer un service" to="/services/creer" noBackground />
  </div>
</CenteredGrid>
