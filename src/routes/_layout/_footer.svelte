<script>
  import { goto } from "$app/navigation";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import NavItem from "$lib/components/nav-item.svelte";

  import LogoRF from "$lib/assets/logo-rf.svg";

  function handleOpenCookiesPanel() {
    tarteaucitron.userInterface.openPanel();
  }
</script>

<footer class="border-t-2 border-france-blue pt-5/2 noprint">
  <CenteredGrid>
    <div class="col-span-5 lg:mb-5">
      <img class="inline" src={LogoRF} alt="" width="124" height="110" />
    </div>
    <div
      class="col-start-1 col-span-full text-sm leading-normal text-gray-text lg:col-span-6 lg:col-start-7"
    >
      Dora est un service public numérique qui permet aux structures de
      l’insertion de référencer simplement et mettre à jour en temps réel leur
      offre de services, et aux professionnels prescripteurs de rechercher et
      mobiliser rapidement le service le plus adapté au besoin de leur
      bénéficiaire.
      <div class="flex gap-x-3 gap-y-1 mt-2 font-bold flex-wrap">
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
    <nav class="flex col-start-1 col-span-full flex-wrap py-2 gap-y-1">
      <NavItem href="" label="Plan du site" separator light />
      <NavItem
        href=""
        label="Mentions légales"
        on:click={() => goto("/mentions-legales")}
        separator
        light
      />
      <NavItem href="" label="Données personnelles" separator light />
      <NavItem
        href=""
        label="Gestion des cookies"
        separator
        light
        on:click={handleOpenCookiesPanel}
      />
      <NavItem href="" label="Accessibilité : non conforme" light />
    </nav>
  </CenteredGrid>
</footer>
