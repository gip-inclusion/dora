<script>
  import Tabs from "$lib/components/tabs.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import SearchByCommune from "$lib/components/structures/search-by-commune.svelte";
  import SearchBySiret from "$lib/components/structures/search-by-siret.svelte";
  import PoleEmploiWarning from "./_pole-emploi-warning.svelte";

  export let blockPoleEmploi = false;
  export let onCityChange = null;
  export let onEstablishmentChange = null;
  export let establishment = null;
  export let siret = "";

  export let tabId = "nom";

  function handleCityChange(newCity) {
    establishment = null;

    if (onCityChange) onCityChange(newCity);
  }

  async function handleEstablishmentChange(newEstablishment) {
    establishment = newEstablishment;

    if (onEstablishmentChange) onEstablishmentChange(newEstablishment);
  }

  function handleTabChange(newTab) {
    establishment = null;
    tabId = newTab;

    if (onEstablishmentChange) onEstablishmentChange(establishment);
  }

  const tabs = [
    { id: "nom", name: "Nom" },
    { id: "siret", name: "Siret" },
  ];

  if (blockPoleEmploi) {
    tabs.push({ id: "pe", name: "Pôle emploi" });
  }

  if (siret) {
    tabId = "siret";
  }
</script>

<FieldSet
  title="Structure"
  headerBg="bg-magenta-brand"
  noHeaderBorder
  noTopPadding
>
  <div slot="description">
    <p class="text-f14 text-white">
      Choisissez une méthode d'identification. En cas de doute,
      <a
        class="underline"
        target="_blank"
        title="Ouverture dans une nouvelle fenêtre"
        rel="noopener nofollow"
        href="https://aide.dora.fabrique.social.gouv.fr/fr/">contactez-nous</a
      >.
    </p>

    <Tabs items={tabs} onSelectedChange={handleTabChange} itemId={tabId} />
  </div>

  {#if tabId === "siret"}
    <SearchBySiret onEstablishmentChange={handleEstablishmentChange} {siret} />
  {:else if tabId === "nom"}
    <SearchByCommune
      bind:establishment
      onEstablishmentChange={handleEstablishmentChange}
      onCityChange={handleCityChange}
    />
  {:else if tabId === "pe"}
    <PoleEmploiWarning />
  {/if}

  {#if blockPoleEmploi && tabId !== "pe" && establishment?.siret.startsWith("130005481")}
    <PoleEmploiWarning />
  {:else}
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
  {/if}
</FieldSet>
