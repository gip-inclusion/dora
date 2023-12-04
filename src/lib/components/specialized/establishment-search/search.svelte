<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import Tabs from "$lib/components/display/tabs.svelte";
  import SearchByCommune from "./search-by-commune.svelte";
  import SearchBySafir from "./search-by-safir.svelte";
  import SearchBySiret from "./search-by-siret.svelte";
  import type { Establishment, GeoApiValue } from "$lib/types";

  export let onCityChange: ((city: GeoApiValue | null) => void) | undefined =
    undefined;
  type Tab = "nom" | "siret" | "safir";

  export let onEstablishmentChange:
    | ((establishment: Establishment | null) => void)
    | undefined = undefined;

  export let establishment: Establishment | null = null;
  export let isOwnStructure = true;
  export let showSafir: boolean = false;
  export let tabId: Tab = showSafir ? "safir" : "nom";

  export let title = "Structure";
  export let description: string | undefined = undefined;
  export let proposedSafir: string;
  export let proposedSiret: string;

  if (!showSafir) {
    proposedSafir = "";
  }

  function handleCityChange(newCity: GeoApiValue | null) {
    establishment = null;

    if (onCityChange) {
      onCityChange(newCity);
    }
  }

  function handleEstablishmentChange(newEstablishment: Establishment | null) {
    establishment = newEstablishment;
    if (onEstablishmentChange) {
      onEstablishmentChange(newEstablishment);
    }
  }

  function handleTabChange(newTab: Tab) {
    if (newTab !== tabId) {
      establishment = null;
      tabId = newTab;
      if (onEstablishmentChange) {
        onEstablishmentChange(establishment);
      }
    }
  }
  const tabs: { id: string; name: string }[] = [];
  if (showSafir) {
    tabs.push({ id: "safir", name: "Agences Pôle emploi" });
  }

  tabs.push(
    ...[
      { id: "nom", name: "Par nom" },
      { id: "siret", name: "Par siret" },
    ]
  );

  if (proposedSiret) {
    tabId = "siret";
  }
</script>

<FieldSet {title} headerBg="bg-magenta-brand" noHeaderBorder noTopPadding>
  <div slot="description">
    <p class="text-f14 text-white">
      {#if description}
        {description}
      {:else}
        Choisissez une méthode d’identification. En cas de doute,
        <a
          class="underline"
          target="_blank"
          title="Ouverture dans une nouvelle fenêtre"
          rel="noopener"
          href="https://aide.dora.inclusion.beta.gouv.fr/fr/">contactez-nous</a
        >.
      {/if}
    </p>

    <Tabs items={tabs} onSelectedChange={handleTabChange} itemId={tabId} />
  </div>

  {#if tabId === "siret"}
    <SearchBySiret
      onEstablishmentChange={handleEstablishmentChange}
      {establishment}
      {proposedSiret}
    />
  {:else if tabId === "nom"}
    <SearchByCommune
      bind:establishment
      onEstablishmentChange={handleEstablishmentChange}
      onCityChange={handleCityChange}
      {isOwnStructure}
    />
  {:else if tabId === "safir"}
    <SearchBySafir
      {establishment}
      onEstablishmentChange={handleEstablishmentChange}
      {proposedSafir}
    />
  {/if}

  {#if establishment?.siret}
    <div class="border border-gray-01 p-s24">
      <h4 class="text-gray-text">{establishment.name}</h4>
      <div class="legend">{establishment.siret}</div>
      <div class="legend">{establishment.address1}</div>
      <div class="legend">{establishment.address2}</div>
      <div class="legend">
        {establishment.postalCode}
        {establishment.city}
      </div>
    </div>
  {/if}
  <slot name="cta" />
</FieldSet>
