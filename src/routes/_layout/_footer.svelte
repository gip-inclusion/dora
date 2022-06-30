<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import NavItem from "$lib/components/nav-item.svelte";

  import LogoRF from "$lib/assets/logo-rf.svg";

  function handleOpenCookiesPanel(evt) {
    evt.preventDefault();
    tarteaucitron.userInterface.openPanel();
  }
</script>

<footer class="noprint border-t-2 border-france-blue">
  <CenteredGrid>
    <div class="flex gap-s24 lg:flex-row">
      <div class="mb-s24 lg:w-1/2">
        <img class="inline" src={LogoRF} alt="" width="124" height="110" />
      </div>
      <div class="text-f14 leading-normal text-gray-text lg:w-1/2">
        Dora, le service public numérique de recensement et mise à jour de
        l’offre d’insertion.
        <div class="mt-s16 flex flex-wrap gap-x-s24 gap-y-s8 font-bold">
          <a target="_blank" rel="noopener" href="https://gouvernement.fr"
            >gouvernement.fr</a
          >
          <a target="_blank" rel="noopener" href="https://service-public.fr"
            >service-public.fr</a
          >
          <a target="_blank" rel="noopener" href="https://data.gouv.fr"
            >data.gouv.fr</a
          >
        </div>
      </div>
    </div>

    <hr class="mb-s16" />

    <nav class="flex flex-wrap gap-s32">
      <NavItem
        href="https://documentation.dora.fabrique.social.gouv.fr/informations-legales/mentions-legales"
        label="Mentions légales"
        otherTab
        nofollow
      />
      <NavItem
        href="https://documentation.dora.fabrique.social.gouv.fr/informations-legales/conditions-generales-dutilisation"
        label="CGU"
        otherTab
        nofollow
      />
      <NavItem
        label="Données personnelles"
        href="https://documentation.dora.fabrique.social.gouv.fr/informations-legales/politique-de-confidentialite"
        otherTab
        nofollow
      />
      <NavItem
        href="#"
        on:click={handleOpenCookiesPanel}
        label="Gestion des cookies"
        otherTab
        nofollow
      />
      <span class="text-f14 text-gray-text-alt2"
        >Accessibilité : non conforme</span
      >
      <NavItem label="Statistiques" href="/stats" />
    </nav>
  </CenteredGrid>
</footer>
