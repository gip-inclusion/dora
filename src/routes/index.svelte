<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
</script>

<CenteredGrid class="row-start-1">
  <div class="col-start-1 col-span-full mb-5">
    <!-- <LinkButton label="Design System" to="design-system" noBackground /> -->
    <LinkButton
      label="Créer une structure"
      to="/structures/creer"
      noBackground />
    <LinkButton label="Créer un service" to="/services/creer" noBackground />
  </div>
</CenteredGrid>
