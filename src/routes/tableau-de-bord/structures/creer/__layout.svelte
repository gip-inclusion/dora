<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
</script>

<EnsureLoggedIn>
  <CenteredGrid topPadded>
    <div class="col-start-1 col-span-full text-center mb-s48">
      <h1 class="text-france-blue">Création d’une structure</h1>
      <p class="text-f16">
        Rendez visible vos offres de services sur la plateforme DORA.
      </p>
    </div>
  </CenteredGrid>

  <CenteredGrid roundedbg>
    <div class="col-span-8 col-start-1 mb-s32">
      <slot />
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
