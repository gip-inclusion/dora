<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import NavItem from "$lib/components/nav-item.svelte";

  import LogoRF from "$lib/assets/logo-rf.svg";

  function handleOpenCookiesPanel(evt) {
    evt.preventDefault();
    tarteaucitron.userInterface.openPanel();
  }
</script>

<footer class="border-t-2 border-france-blue pt-s20 noprint">
  <CenteredGrid>
    <div class="col-span-5 lg:mb-s40">
      <img class="inline" src={LogoRF} alt="" width="124" height="110" />
    </div>
    <div
      class="col-start-1 col-span-full text-f14 leading-normal text-gray-text lg:col-span-6 lg:col-start-7"
    >
      Dora est un service public numérique qui permet aux structures de
      l’insertion de référencer simplement et mettre à jour en temps réel leur
      offre de services, et aux professionnels prescripteurs de rechercher et
      mobiliser rapidement le service le plus adapté au besoin de leur
      bénéficiaire.
      <div class="flex gap-x-s24 gap-y-s8 mt-s16 font-bold flex-wrap">
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
    <nav class="flex col-start-1 col-span-full flex-wrap py-s16 gap-y-s8">
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
