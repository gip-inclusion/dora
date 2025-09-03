<script lang="ts">
  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";
  import SubMenuDropdown from "./sub-menu-dropdown.svelte";

  interface Props {
    mobileDesign?: boolean;
    externalIconColor?: string;
    aClass?: string;
  }

  let {
    mobileDesign = false,
    externalIconColor = mobileDesign ? "text-magenta-cta" : "text-gray-text",
    aClass = mobileDesign
      ? "py-s16 text-f18 font-bold text-gray-dark"
      : "text-f14 text-gray-text p-s16",
  }: Props = $props();
</script>

<div class="{mobileDesign ? 'hidden' : 'block'} py-s10 md:hidden">
  <div class="text-f20 text-gray-dark font-bold">DORA</div>
  <div class="text-f14 text-gray-text">Plateforme de l’inclusion</div>
</div>

<nav class="{mobileDesign ? 'block' : 'hidden'} md:block">
  <ul class={mobileDesign ? "flex flex-col" : "inline-flex"}>
    <li
      class="border-gray-03 leading-24 lg:border-none"
      class:border-b={mobileDesign}
    >
      <a href="/" class="inline-block h-full {aClass}">
        Recherche par besoins
      </a>
    </li>

    <li
      class="border-gray-03 leading-24 lg:border-none"
      class:border-b={mobileDesign}
    >
      <a href="/recherche-textuelle" class="inline-block h-full {aClass}">
        Recherche par mots-clés 🆕
      </a>
    </li>

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
            openInNewTab: true,
          },
          {
            href: "https://aide.dora.inclusion.beta.gouv.fr/fr/article/participer-a-un-webinaire-dora-h3n747/",
            label: "Webinaires",
          },
          {
            href: "https://docs.google.com/presentation/d/e/2PACX-1vQ1xdf83eiY7CVTcWLpOg9cE8Zjd_9oEVe4RCeia9FNNB7FnTYXX6S21nbsMV3es6zgIwhwgKODI8dk/pub?start=false&loop=false&delayms=3000",
            label: "Kit de déploiement",
            openInNewTab: true,
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
          class="h-s20 w-s20 pl-s4 pt-s6 inline-block fill-current {externalIconColor}"
          aria-hidden="true"
        >
          <ExternalLinkLineSystem size="16" />
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
          class="h-s20 w-s20 pl-s4 pt-s6 inline-block fill-current {externalIconColor}"
          aria-hidden="true"
        >
          <ExternalLinkLineSystem size="16" />
        </span>
      </a>
    </li>
  </ul>
</nav>
