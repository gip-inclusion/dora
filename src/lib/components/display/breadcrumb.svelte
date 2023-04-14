<script lang="ts">
  // Source pour l'accessibilité : https://www.systeme-de-design.gouv.fr/elements-d-interface/composants/fil-d-ariane
  import type { Service, Structure } from "$lib/types";

  type BreadcrumbLocation =
    | "home"
    | "search"
    | "legal"
    | "cgu"
    | "account"
    | "login"
    | "accessibility"
    | "privacy"
    | "partners"
    | "structure-informations"
    | "structure-collaborateurs"
    | "structure-services"
    | "structure-modeles"
    | "structure-antennes"
    | "service";

  export let structure: Structure | undefined = undefined;
  export let service: Service | undefined = undefined;
  export let currentLocation: BreadcrumbLocation;
  export let dark = false;

  const locationToText: Record<string, string> = {
    search: "Recherche",
    login: "Accéder à DORA",
    legal: "Mentions légales",
    cgu: "Conditions générales d’utilisation",
    accessibility: "Accessibilité",
    privacy: "Données personnelles",
    partners: "Nos partenaires",
    account: "Mes informations",
  };

  function getStructureData(location) {
    if (location === "structure-collaborateurs") {
      return {
        url: "collaborateurs",
        name: "Collaborateurs",
      };
    } else if (location === "structure-services") {
      return {
        url: "services",
        name: "Services",
      };
    } else if (location === "structure-modeles") {
      return {
        url: "modeles",
        name: "Modèles",
      };
    } else if (location === "structure-antennes") {
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

  $: structureData = getStructureData(currentLocation);
</script>

<nav aria-label="vous êtes ici :" class="print:hidden" class:dark>
  <ol class="text-f14">
    <li class="inline">
      {#if currentLocation === "home"}
        <a aria-current="page" class="current">Accueil</a>
      {:else}
        <a href="/" title="Retour à l'accueil du site">Accueil</a>
      {/if}
    </li>

    {#if structure}
      <li class="inline before:content-['/']">
        <a
          href={currentLocation === "structure-informations"
            ? null
            : `/structures/${structure.slug}`}
          class:current={currentLocation === "structure-informations"}
          aria-current={currentLocation === "structure-informations"
            ? "page"
            : null}
        >
          <span class="hidden lg:inline">
            Structure&nbsp;•&nbsp;
          </span>{structure.name}
        </a>
      </li>
    {/if}

    {#if Object.keys(locationToText).includes(currentLocation)}
      <li class="inline before:content-['/']">
        <a aria-current="page" class="current">
          {locationToText[currentLocation]}
        </a>
      </li>
    {/if}

    {#if service}
      <li class="inline before:content-['/']">
        <a
          href={currentLocation === "service"
            ? null
            : `/services/${service.slug}`}
          class:current={currentLocation === "service"}
          aria-current={currentLocation === "service" ? "page" : null}
        >
          <span class="hidden lg:inline">Service&nbsp;•&nbsp;</span>
          {service.name}
        </a>
      </li>
    {:else if currentLocation.startsWith("structure-") && currentLocation !== "structure-informations"}
      <li class="inline before:content-['/']">
        <a class="current" aria-current="page">
          {structureData.name}
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

  .dark a {
    @apply text-gray-text;
  }
  .dark li::before,
  .dark .current {
    @apply text-gray-text;
  }
</style>
