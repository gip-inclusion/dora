<script lang="ts">
  // Source pour l'accessibilité : https://www.systeme-de-design.gouv.fr/elements-d-interface/composants/fil-d-ariane
  import type { Model, Service, Structure } from "$lib/types";

  type BreadcrumbLocation =
    | "home"
    | "search"
    | "legal"
    | "cgu"
    | "model"
    | "saved-searches"
    | "saved-search"
    | "bookmarks"
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
    | "service-orientation"
    | "service-orientation-step1"
    | "service-orientation-step2"
    | "service-orientation-confirmation"
    | "orientation"
    | "service"
    | "manager-dashboard";

  export let structure: Structure | undefined = undefined;
  export let service: Service | undefined = undefined;
  export let model: Model | undefined = undefined;
  export let currentLocation: BreadcrumbLocation | string;
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
    "service-orientation": "Orienter",
    "service-orientation-step1": "Orienter • Étape 1/2",
    "service-orientation-step2": "Orienter • Étape 2/2",
    "service-orientation-confirmation": "Orienter • Confirmation",
    orientation: "Demande d’orientation",
    "saved-searches": "Mes alertes",
    "saved-search": "Mon alerte",
    bookmarks: "Mes favoris",
    "manager-dashboard": "Gestion du territoire",
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

  $: linkClasses = `${dark ? "text-gray-text" : "text-magenta-40"} print:text-france-blue`;
  $: currentClasses = `font-bold ${dark ? "text-gray-text" : "text-white"} print:text-france-blue`;
</script>

<nav aria-label="vous êtes ici :" class="print:hidden" class:dark>
  <ol class="text-f14">
    <li class="inline">
      {#if currentLocation === "home"}
        <span aria-current="page" class={currentClasses}>Accueil</span>
      {:else}
        <a href="/" class={linkClasses} title="Retour à l’accueil du site"
          >Accueil</a
        >
      {/if}
    </li>

    {#if structure}
      <li class="inline before:content-['/']">
        {#if structure.slug}
          {#if currentLocation === "structure-informations"}
            <span class={currentClasses} aria-current="page">
              <span class="hidden lg:inline">
                Structure&nbsp;•&nbsp;</span
              >{structure.name}
            </span>
          {:else}
            <a href="/structures/{structure.slug}" class={linkClasses}>
              <span class="hidden lg:inline">
                Structure&nbsp;•&nbsp;</span
              >{structure.name}
            </a>
          {/if}
        {:else}
          <span
            class="print:text-france-blue hidden text-white lg:inline"
            class:text-gray-text={dark}
          >
            Structure&nbsp;•&nbsp;
          </span><span
            class=" print:text-france-blue text-white lg:inline"
            class:text-gray-text={dark}>{structure.name}</span
          >
        {/if}
      </li>
    {/if}

    {#if service}
      <li class="inline before:content-['/']">
        {#if currentLocation === "service"}
          <span class={currentClasses} aria-current="page">
            <span class="hidden lg:inline">Service&nbsp;•&nbsp;</span
            >{service.name}
          </span>
        {:else}
          <a href="/services/{service.slug}" class={linkClasses}>
            <span class="hidden lg:inline">Service&nbsp;•&nbsp;</span
            >{service.name}
          </a>
        {/if}
      </li>
    {:else if currentLocation.startsWith("structure-") && currentLocation !== "structure-informations"}
      <li class="inline before:content-['/']">
        <span class={currentClasses} aria-current="page">
          {structureData.name}
        </span>
      </li>
    {/if}
    {#if currentLocation === "saved-search"}
      <li class="inline before:content-['/']">
        <a href="/mes-alertes" class={linkClasses}>
          <span class="hidden lg:inline">Mes alertes</span>
        </a>
      </li>
    {/if}
    {#if Object.keys(locationToText).includes(currentLocation)}
      <li class="inline before:content-['/']">
        <span aria-current="page" class={currentClasses}>
          {locationToText[currentLocation]}
        </span>
      </li>
    {/if}

    {#if model}
      <li class="inline before:content-['/']">
        {#if currentLocation === "model"}
          <span class={currentClasses} aria-current="page">
            <span class="hidden lg:inline">Modèle&nbsp;•&nbsp;</span
            >{model.name}
          </span>
        {:else}
          <a href="/modeles/{model.slug}" class={linkClasses}>
            <span class="hidden lg:inline">Modèle&nbsp;•&nbsp;</span
            >{model.name}
          </a>
        {/if}
      </li>
    {/if}
  </ol>
</nav>

<style lang="postcss">
  @reference "../../../app.css";

  nav li + li::before {
    @apply ml-s8 mr-s8 text-magenta-40 inline;
  }

  .dark li::before {
    @apply text-gray-text;
  }
</style>
