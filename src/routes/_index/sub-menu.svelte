<script lang="ts">
  import { externalLinkIcon } from "$lib/icons";
  import SubMenuDropdown from "./sub-menu-dropdown.svelte";

  export let mobileDesign = false;
  export let externalIconColor = mobileDesign
    ? "text-magenta-cta"
    : "text-gray-text";

  export let aClass = mobileDesign
    ? "py-s16 text-f18 font-bold text-gray-dark"
    : "text-f14 text-gray-text p-s16";
</script>

<div class="{mobileDesign ? 'hidden' : 'block'} py-s10 md:hidden">
  <div class="text-f20 font-bold text-gray-dark">DORA</div>
  <div class="text-f14 text-gray-text">Plateforme de l’inclusion</div>
</div>

<nav class="{mobileDesign ? 'block' : 'hidden'} md:block">
  <ul class={mobileDesign ? "flex flex-col" : "inline-flex"}>
    <li>
      <SubMenuDropdown
        {mobileDesign}
        label="Contribuer"
        links={[
          {
            href: "https://tally.so/r/nGegBe",
            label: "Inviter une structure partenaire",
          },
          {
            href: "/contribuer",
            label: "Suggérer le service d’un partenaire",
          },
          {
            href: "/services/creer",
            label: "Référencer vos services",
          },
        ]}
      />
    </li>

    <li>
      <SubMenuDropdown
        {mobileDesign}
        label="Ressources"
        links={[
          {
            href: "https://www.youtube.com/channel/UCadIsy9gfHgLmLkutRGC5ew/playlists",
            label: "Tutoriels vidéo",
          },
          {
            href: "https://app.livestorm.co/dora-1",
            label: "Webinaires",
          },
          {
            href: "https://aide.dora.inclusion.beta.gouv.fr/fr/article/deployer-la-plateforme-dora-sur-votre-territoire-qb9ner/",
            label: "Kit de déploiement",
          },
          {
            href: "https://aide.dora.inclusion.beta.gouv.fr/fr/article/kit-de-communication-1x9t4kj/",
            label: "Kit de communication",
          },
        ]}
      />
    </li>

    <li class="border-gray-03 lg:border-none" class:border-b={mobileDesign}>
      <a
        target="_blank"
        title="Ouverture dans une nouvelle fenêtre"
        rel="noopener"
        href="https://aide.dora.inclusion.beta.gouv.fr/fr/category/quoi-de-neuf-es1img/"
        class="inline-block h-full {aClass}"
      >
        Nouveautés
        <span
          class="inline-block h-s20 w-s20 fill-current pt-s6 pl-s4 {externalIconColor}"
          aria-hidden
        >
          {@html externalLinkIcon}
        </span>
      </a>
    </li>

    <li class="border-gray-03 lg:border-none" class:border-b={mobileDesign}>
      <a
        target="_blank"
        title="Ouverture dans une nouvelle fenêtre"
        rel="noopener"
        href="https://communaute.inclusion.beta.gouv.fr/forum/dora-105/"
        class="inline-block h-full {aClass}"
      >
        Communauté de l’inclusion
        <span
          class="inline-block h-s20 w-s20 fill-current pt-s6 pl-s4 {externalIconColor}"
          aria-hidden
        >
          {@html externalLinkIcon}
        </span>
      </a>
    </li>
  </ul>
</nav>
