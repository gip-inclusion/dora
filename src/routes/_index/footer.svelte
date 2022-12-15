<script lang="ts">
  import LogoRF from "$lib/assets/logos/logo-rf.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import NavItem from "$lib/components/display/nav-item.svelte";

  function handleOpenCookiesPanel(evt) {
    evt.preventDefault();
    window.tarteaucitron.userInterface.openPanel();
  }
</script>

<footer class="border-t-2 border-france-blue print:hidden">
  <CenteredGrid>
    <div class="flex gap-s24 lg:flex-row">
      <div class="mb-s24 lg:w-1/2">
        <img
          class="inline"
          src={LogoRF}
          alt="République Française - Liberté, Égalité, Fraternité"
          width="124"
          height="110"
        />
      </div>
      <div class="text-f14 leading-normal text-gray-text lg:w-1/2">
        Dora, le service public numérique de recensement et mise à jour de
        l’offre d’insertion.
        <div class="mt-s16 flex flex-wrap gap-x-s24 gap-y-s8 font-bold">
          <a
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener"
            href="https://gouvernement.fr">gouvernement.fr</a
          >
          <a
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener"
            href="https://service-public.fr">service-public.fr</a
          >
          <a
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener"
            href="https://data.gouv.fr">data.gouv.fr</a
          >
        </div>
      </div>
    </div>

    <hr class="mb-s16" />

    <nav class="flex flex-wrap gap-s32">
      <NavItem href="/mentions-legales" label="Mentions légales" />
      <NavItem href="/cgu" label="CGU" />
      <NavItem
        label="Données personnelles"
        href="/politique-de-confidentialite"
      />
      <NavItem
        href="#"
        on:click={handleOpenCookiesPanel}
        label="Gestion des cookies"
      />
      <NavItem label="Accessibilité : non conforme" href="/accessibilite" />

      <NavItem label="Statistiques" href="/stats" />
    </nav>
  </CenteredGrid>
</footer>
