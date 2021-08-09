<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
</script>

<CenteredGrid class1="row-start-1">
  <div class="col-start-1 col-span-full">
    <LinkButton label="Design System" to="design-system" noBackground />
    <LinkButton
      label="Création de structure"
      to="/structures/creer"
      noBackground />
    <LinkButton label="Création de service" to="/services/creer" noBackground />
  </div>
</CenteredGrid>
