<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <div class="col-start-1 col-span-full text-center mb-6">
      <h1 class="text-france-blue text-13xl">Création d’une structure</h1>
      <p class="text-gray-text text-base">
        Rendez visible vos offres de services sur la plateforme DORA.
      </p>
    </div>
  </CenteredGrid>

  <CenteredGrid gridRow="2" roundedbg>
    <div class="col-span-8 col-start-1 mb-4">
      <slot />
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
