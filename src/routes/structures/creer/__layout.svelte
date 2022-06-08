<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1 class="text-france-blue">Création d’une structure</h1>
  </CenteredGrid>

  <CenteredGrid bgColor="bg-gray-bg">
    <slot />
  </CenteredGrid>
</EnsureLoggedIn>
