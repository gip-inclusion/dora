<script lang="ts">
  import NewspaperLineDocument from "svelte-remix/NewspaperLineDocument.svelte";

  import LogoRF from "$lib/assets/logos/logo-rf.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import NavItem from "$lib/components/display/nav-item.svelte";
  import { showCookieBanner } from "$lib/utils/consent.svelte";
</script>

<hr class="border-t-gray-01 print:hidden" />

<CenteredGrid noPadding>
  <div
    class="py-s32 flex flex-col items-center justify-between lg:flex-row print:hidden"
  >
    <div class="text-f14 text-gray-dark">
      <strong>Infolettre &nbsp;•&nbsp;</strong>
      Une fois par mois, recevez un courriel pour être informé des évolutions de DORA.
    </div>

    <LinkButton
      label="S’abonner à l’infolettre"
      icon={NewspaperLineDocument}
      iconOnRight
      noBackground
      small
      to="https://d4c653e7.sibforms.com/serve/MUIEAEkY4naptXBIq5NdRg5UPxP1wmwbGCinne5c1gynY-wfrZ0Dz0QP_NqkXtfyYqhdaq3AO8VFZJ9giRi9ZT0eah7Ut2U0LeKSTVIHQb_5nhvTLUMWXo9ZMeIYCHVlzmjkXGQ66S5ewcYpSADUgV--2RVZ_mrnsRJQoCNwZ8y-sWzfQsEzfKuTA7SLbZ_dWeqaigudym3EaiHT"
      otherTab
    />
  </div>
</CenteredGrid>
<footer class="border-france-blue border-t-2 print:hidden">
  <CenteredGrid>
    <div class="gap-s24 flex lg:flex-row">
      <div class="mb-s24 lg:w-1/2">
        <img
          class="inline"
          src={LogoRF}
          alt="République Française - Liberté, Égalité, Fraternité"
          width="124"
          height="110"
        />
      </div>
      <div class="text-f14 text-gray-text leading-normal lg:w-1/2">
        Dora, le service public numérique de recensement et mise à jour de
        l’offre d’insertion.
        <div class="mt-s16 gap-x-s24 gap-y-s8 flex flex-wrap font-bold">
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

    <nav class="gap-s32 flex flex-wrap">
      <NavItem href="/mentions-legales" label="Mentions légales" />
      <NavItem href="/cgu" label="Conditions générales d’utilisation" />
      <NavItem
        label="Données personnelles"
        href="/politique-de-confidentialite"
      />
      <NavItem label="Gestion des cookies" onclick={showCookieBanner} />
      <NavItem label="Accessibilité : non conforme" href="/accessibilite" />

      <NavItem label="Statistiques" href="/stats" />
    </nav>
  </CenteredGrid>
</footer>
