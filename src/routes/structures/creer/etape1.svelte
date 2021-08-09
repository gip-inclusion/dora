<script>
  import { structureCache, structureOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";

  import CustomLayout from "./_custom-layout.svelte";

  import NavButtons from "./_nav.svelte";

  import SiretSearch from "./_siret_search.svelte";
  import CitySearch from "./_city_search.svelte";

  let selectedCity;

  $: console.log($structureOptions);
  $: console.log($structureCache);

  function handleCityChange(city) {
    console.log("handleCityChange");
    selectedCity = city;
    console.log(selectedCity);
  }

  function handleEstablishmentChange(establishment) {
    console.log("handleEstablishmentChange", establishment);
    $structureCache.siret = establishment.siret;
    $structureCache.name = establishment.name || establishment.parent;
    $structureCache.address1 = establishment.addr1;
    $structureCache.address2 = establishment.addr2;
    $structureCache.city = (
      (establishment.city || "") +
      " " +
      (establishment.distrib || "")
    ).trim();
    $structureCache.cityCode = establishment.citycode;
    $structureCache.postalCode = establishment.postcode;
    $structureCache.ape = establishment.ape;
    $structureCache.longitude = establishment.longitude;
    $structureCache.latitude = establishment.latitude;
  }
</script>

<CustomLayout>
  <svelte:fragment slot="content">
    {#if $structureOptions}
      <FieldSet title="">
        <CitySearch selectedCity handleChange={handleCityChange} />
        <SiretSearch
          selectedEstablishment
          {selectedCity}
          disabled={!selectedCity?.value?.properties?.citycode}
          handleChange={handleEstablishmentChange} />
      </FieldSet>

      <FieldSet title="Présentez votre Structure">
        <ModelField
          type="text"
          field={$structureOptions.siret}
          disabled
          bind:value={$structureCache.siret} />
        <ModelField
          type="text"
          field={$structureOptions.name}
          bind:value={$structureCache.name} />
        <ModelField
          type="text"
          field={$structureOptions.shortDesc}
          bind:value={$structureCache.shortDesc} />
        <ModelField
          type="hidden"
          field={$structureOptions.address1}
          bind:value={$structureCache.address1} />
        <ModelField
          type="hidden"
          field={$structureOptions.address2}
          bind:value={$structureCache.address2} />
        <ModelField
          type="hidden"
          field={$structureOptions.city}
          bind:value={$structureCache.city} />
        <ModelField
          type="hidden"
          field={$structureOptions.cityCode}
          bind:value={$structureCache.cityCode} />
        <ModelField
          type="hidden"
          field={$structureOptions.postalCode}
          bind:value={$structureCache.postalCode} />
        <ModelField
          type="hidden"
          field={$structureOptions.ape}
          bind:value={$structureCache.ape} />
        <ModelField
          type="hidden"
          field={$structureOptions.longitude}
          bind:value={$structureCache.longitude} />
        <ModelField
          type="hidden"
          field={$structureOptions.latitude}
          bind:value={$structureCache.latitude} />
      </FieldSet>
    {/if}
  </svelte:fragment>
  <svelte:fragment slot="navbar">
    <NavButtons withValidate />
  </svelte:fragment>
</CustomLayout>
