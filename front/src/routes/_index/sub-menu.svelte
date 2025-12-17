<script lang="ts">
  import SubMenuDropdown from "./sub-menu-dropdown.svelte";

  interface Props {
    mobileDesign?: boolean;
    externalIconColor?: string;
    aClass?: string;
  }

  let {
    mobileDesign = false,
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
        Recherche par mots-clés
      </a>
    </li>
    <li
      class="border-gray-03 leading-24 lg:border-none"
      class:border-b={mobileDesign}
    >
      <a href="/orientations/suivi" class="inline-block h-full {aClass}">
        Suivi des orientations 🆕
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
            href: "/services/creer",
            label: "Référencer vos services",
          },
        ]}
      />
    </li>
  </ul>
</nav>
