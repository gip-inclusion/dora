<script lang="ts">
  // Source pour l'accessibilité : https://www.w3.org/WAI/ARIA/apg/example-index/breadcrumb/index.html
  import { page } from "$app/stores";
  import type { Service, Structure } from "$lib/types";

  type BreadcrumbLocation =
    | "home"
    | "search"
    | "structure-informations"
    | "structure-collaborateurs"
    | "structure-services"
    | "structure-modeles"
    | "structure-antennes"
    | "service";

  export let structure: Structure | undefined = undefined;
  export let service: Service | undefined = undefined;
  export let currentLocation: BreadcrumbLocation;

  $: structureData = getStructureData(currentLocation);

  function getStructureData(currentLocation) {
    if (currentLocation === "structure-collaborateurs") {
      return {
        url: "collaborateurs",
        name: "Collaborateurs",
      };
    } else if (currentLocation === "structure-services") {
      return {
        url: "services",
        name: "Services",
      };
    } else if (currentLocation === "structure-modeles") {
      return {
        url: "modeles",
        name: "Modèles",
      };
    } else if (currentLocation === "structure-antennes") {
      return {
        url: "antennes",
        name: "Antennes",
      };
    }

    return {
      url: "",
      name: "",
    };
  }
</script>

<nav
  aria-label="Fil d'ariane"
  class="print:hidden"
  class:search-style={currentLocation === "search"}
>
  <ol class="text-f14">
    <li class="inline">
      <a
        href={"/"}
        aria-current={currentLocation === "home" ? "page" : null}
        class:current={currentLocation === "home"}
        title="Retour à l'accueil du site">Accueil</a
      >
    </li>

    {#if structure}
      <li class="inline before:content-['/']">
        <a
          href="/structures/{structure.slug}"
          class:current={currentLocation === "structure-informations"}
          aria-current={currentLocation === "structure-informations"
            ? "page"
            : null}
        >
          <span class="hidden lg:inline"
            >Structure&nbsp;•&nbsp;
          </span>{structure.name}
        </a>
      </li>
    {/if}

    {#if currentLocation === "search"}
      <li class="inline before:content-['/']">
        <a href={$page.url.href} aria-current="page" class="current">
          Recherche
        </a>
      </li>
    {/if}

    {#if service}
      <li class="inline before:content-['/']">
        <a
          href="/services/{service.slug}"
          class:current={currentLocation === "service"}
          aria-current={currentLocation === "service" ? "page" : null}
          ><span class="hidden lg:inline">Service&nbsp;•&nbsp;</span
          >{service.name}</a
        >
      </li>
    {:else if currentLocation.startsWith("structure-") && currentLocation !== "structure-informations"}
      <li class="inline before:content-['/']">
        <a
          href="/structures/{structure.slug}/{structureData.url}"
          class="current"
          aria-current="page"
        >
          <span>{structureData.name}</span>
        </a>
      </li>
    {/if}
  </ol>
</nav>

<style lang="postcss">
  a {
    @apply text-magenta-40 print:text-france-blue;
  }

  .current {
    @apply font-bold text-white print:text-france-blue;
  }

  nav li + li::before {
    @apply ml-s8 mr-s8 inline text-magenta-40 print:text-france-blue;
  }

  .search-style a {
    @apply text-gray-text-alt2;
  }
  .search-style li::before,
  .search-style .current {
    @apply text-gray-text;
  }
</style>
