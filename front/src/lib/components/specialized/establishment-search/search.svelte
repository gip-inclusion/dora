<script lang="ts">
  import type { Snippet } from "svelte";

  import FieldSet from "$lib/components/display/fieldset.svelte";
  import Tabs from "$lib/components/display/tabs.svelte";
  import SearchByCommune from "./search-by-commune.svelte";
  import SearchBySafir from "./search-by-safir.svelte";
  import SearchBySiret from "./search-by-siret.svelte";
  import type { Establishment, GeoApiValue } from "$lib/types";
  import { URL_HELP_SITE } from "$lib/consts";

  type Tab = "nom" | "siret" | "safir";

  interface Props {
    onCityChange?: (city: GeoApiValue | null) => void;
    onEstablishmentChange?: (establishment: Establishment | null) => void;
    establishment?: Establishment | null;
    showSafir?: boolean;
    tabId?: Tab;
    title?: string;
    descriptionText?: string;
    proposedSafir?: string | null;
    proposedSiret?: string | null;
    cta?: Snippet;
  }

  let {
    onCityChange,
    onEstablishmentChange,
    establishment = $bindable(),
    showSafir = false,
    tabId = $bindable(showSafir ? "safir" : "nom"),
    title = "Structure",
    descriptionText,
    proposedSafir = $bindable(""),
    proposedSiret = "",
    cta,
  }: Props = $props();

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
    tabs.push({ id: "safir", name: "Agences France Travail" });
  }

  tabs.push(
    ...[
      { id: "nom", name: "Nom" },
      { id: "siret", name: "SIRET" },
    ]
  );

  if (proposedSiret) {
    tabId = "siret";
  }
</script>

<FieldSet {title} headerBg="bg-magenta-brand" noHeaderBorder noTopPadding>
  {#snippet description()}
    <div>
      <p class="m-s0 text-f14 text-white">
        {#if descriptionText}
          {descriptionText}
        {:else}
          Veuillez choisir une méthode d’identification parmi les options
          disponibles. Si vous rencontrez des difficultés ou avez besoin
          d’assistance, n’hésitez pas à
          <a
            class="underline"
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener"
            href={`${URL_HELP_SITE}/`}>nous contacter</a
          >.
        {/if}
      </p>

      <Tabs items={tabs} onSelectedChange={handleTabChange} itemId={tabId} />
    </div>
  {/snippet}

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
    />
  {:else if tabId === "safir"}
    <SearchBySafir
      {establishment}
      onEstablishmentChange={handleEstablishmentChange}
      {proposedSafir}
    />
  {/if}

  {#if establishment?.siret}
    <div class="border-gray-01 p-s24 border">
      <h4 class="text-f16">{establishment.name}</h4>
      <div class="legend">{establishment.siret}</div>
      <div class="legend">{establishment.address1}</div>
      <div class="legend">{establishment.address2}</div>
      <div class="legend">
        {establishment.postalCode}
        {establishment.city}
      </div>
    </div>
  {/if}
  {@render cta?.()}
</FieldSet>
