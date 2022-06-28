<script>
  import Tabs from "$lib/components/tabs.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import SearchByCommune from "$lib/components/structures/search-by-commune.svelte";
  import SearchBySiret from "$lib/components/structures/search-by-siret.svelte";
  import SearchBySafir from "$lib/components/structures/search-by-safir.svelte";
  import Button from "../button.svelte";

  export let onCityChange = null;
  export let onEstablishmentChange = null;
  export let onValidate = null;
  export let establishment = null;
  export let hasValidation = false;
  export let hasSafir = false;
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

  if (hasSafir) {
    tabs.push({ id: "safir", name: "Safir" });
  }

  if (siret) {
    tabId = "siret";
  }
</script>

<FieldSet
  title="Structure"
  headerBg="bg-france-blue"
  noHeaderBorder
  noTopPadding
>
  <div slot="description">
    <p class="text-f14 text-white">
      Choisissez une méthode d'identification. En cas de doute, <a
        class="underline"
        href="https://itou.typeform.com/doracontactsupp">contactez-nous</a
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
  {:else if hasSafir && tabId === "safir"}
    <SearchBySafir
      bind:establishment
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

  {#if establishment?.siret && hasValidation}
    <div class="mt-s24">
      <div class="legend">
        En cliquant sur <span class="italic">Adhérer à la structure</span>, je
        déclare faire partie de la structure mentionnée ci-dessus et j’atteste
        connaître les risques encourus en cas de faux et d’usage de faux.
      </div>

      <div class="mt-s24 flex justify-end">
        <Button
          label="Adhérer à la structure"
          on:click={onValidate}
          preventDefaultOnMouseDown
        />
      </div>
    </div>
  {/if}
</FieldSet>
