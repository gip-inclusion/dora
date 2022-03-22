<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import NavItem from "$lib/components/nav-item.svelte";

  import LogoRF from "$lib/assets/logo-rf.svg";

  function handleOpenCookiesPanel(evt) {
    evt.preventDefault();
    tarteaucitron.userInterface.openPanel();
  }
</script>

<footer class="noprint border-t-2 border-france-blue pt-s20">
  <CenteredGrid>
    <div class="col-span-5 lg:mb-s40">
      <img class="inline" src={LogoRF} alt="" width="124" height="110" />
    </div>
    <div
      class="col-span-full col-start-1 text-f14 leading-normal text-gray-text lg:col-span-6 lg:col-start-7"
    >
      Dora, le service public numérique de recensement et mise à jour de l’offre
      d’insertion.
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
  </CenteredGrid>
  <CenteredGrid bordertop topPadded>
    <nav class="col-span-full col-start-1 flex flex-wrap gap-y-s8 py-s16">
      <NavItem
        href="https://documentation.dora.fabrique.social.gouv.fr/informations-legales/mentions-legales"
        label="Mentions légales"
        separator
        light
        otherTab
        nofollow
      />
      <NavItem
        href="https://documentation.dora.fabrique.social.gouv.fr/informations-legales/conditions-generales-dutilisation"
        label="CGU"
        separator
        light
        otherTab
        nofollow
      />
      <NavItem
        label="Données personnelles"
        href="https://documentation.dora.fabrique.social.gouv.fr/informations-legales/politique-de-confidentialite"
        separator
        light
        otherTab
        nofollow
      />
      <NavItem
        href="#"
        on:click={handleOpenCookiesPanel}
        label="Gestion des cookies"
        separator
        light
        otherTab
        nofollow
      />
      <NavItem label="Accessibilité : non conforme" light />
    </nav>
  </CenteredGrid>
</footer>
