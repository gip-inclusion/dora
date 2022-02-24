<script>
  import Tabs from "$lib/components/tabs.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import SearchBySiret from "$lib/components/structures/search-by-siret.svelte";

  import SearchByCommune from "$lib/components/structures/search-by-commune.svelte";

  export let onCityChange = null;
  export let onEstablishmentChange = null;

  let establishment = {};

  function handleCityChange(newCity) {
    establishment = {};

    if (onCityChange) onCityChange(newCity);
  }

  async function handleEstablishmentChange(newEstablishment) {
    establishment = newEstablishment;
    if (onEstablishmentChange) onEstablishmentChange(newEstablishment);
  }

  let structureSearchTabId = "siret";
  const structureSearchTabs = [
    { id: "siret", name: "Siret" },
    { id: "nom", name: "Nom" },
  ];

  function handleSelectedTabChange(newTab) {
    establishment = {};
    structureSearchTabId = newTab;
  }
</script>

<FieldSet
  title="Identifiez la structure"
  headerBg="bg-france-blue"
  noHeaderBorder
>
  <div slot="description">
    <p class="text-f14 text-white">
      Choisissez une méthode d'identification. En cas de doute, <a
        class="underline"
        href="https://itou.typeform.com/doracontactsupp">contactez-nous</a
      >.
    </p>

    <Tabs
      items={structureSearchTabs}
      onSelectedChange={handleSelectedTabChange}
      itemId={structureSearchTabId}
    />
  </div>

  {#if structureSearchTabId === "siret"}
    <SearchBySiret onEstablishmentChange={handleEstablishmentChange} />
  {:else if structureSearchTabId === "nom"}
    <SearchByCommune
      onEstablishmentChange={handleEstablishmentChange}
      onCityChange={handleCityChange}
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
</FieldSet>
