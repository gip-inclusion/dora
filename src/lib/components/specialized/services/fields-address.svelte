<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import AddressSearchField from "$lib/components/inputs/address-search-field.svelte";
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
  import CitySearchField from "$lib/components/inputs/city-search-field.svelte";
  import HiddenField from "$lib/components/inputs/hidden-field.svelte";
  import { refreshIcon } from "$lib/icons";
  import type { Service, Structure } from "$lib/types";
  import type { Schema } from "$lib/validation/schemas/utils";

  export let entity: Service | Structure;
  export let parent: Structure | null = null;
  export let schema: Schema;

  function handleAddressChange(address) {
    const props = address?.properties;
    const coords = address?.geometry.coordinates;
    const lat = coords?.[1];
    const long = coords?.[0];
    entity.address1 = props?.name;
    entity.postalCode = props?.postcode;
    entity.longitude = long;
    entity.latitude = lat;
  }

  async function fillAddress() {
    if (parent) {
      const {
        city,
        address1,
        address2,
        postalCode,
        cityCode,
        latitude,
        longitude,
      } = parent;
      entity.city = city;
      entity.address1 = address1;
      entity.address2 = address2;
      entity.postalCode = postalCode;
      entity.cityCode = cityCode;
      entity.latitude = latitude;
      entity.longitude = longitude;
    }
  }

  function handleCityChange(city) {
    entity.city = city?.name;
    entity.cityCode = city?.code;
  }
</script>

{#key entity}
  <div class="flex flex-col">
    {#if parent}
      <div class="mb-s8 lg:w-3/4 lg:self-end">
        <Button
          on:click={fillAddress}
          icon={refreshIcon}
          noBackground
          small
          label="Utiliser les coordonnées de la structure"
        />
      </div>
    {/if}
    <CitySearchField
      id="city"
      schema={schema.city}
      initialValue={entity.city}
      onChange={handleCityChange}
      placeholder="Saisissez et validez votre ville"
    />
  </div>
  <AddressSearchField
    id="address1"
    schema={schema.address1}
    initialValue={entity.address1}
    onChange={handleAddressChange}
    cityCode={entity.cityCode}
    placeholder="3 rue du parc"
    disabled={!entity.cityCode}
  />

  <BasicInputField
    id="address2"
    schema={schema.address2}
    bind:value={entity.address2}
    placeholder="batiment, escalier, etc."
  />

  <BasicInputField
    id="postalCode"
    schema={schema.postalCode}
    bind:value={entity.postalCode}
    placeholder="00000"
  />

  <HiddenField
    id="cityCode"
    schema={schema.cityCode}
    bind:value={entity.cityCode}
  />

  <HiddenField
    id="longitude"
    schema={schema.longitude}
    bind:value={entity.longitude}
  />

  <HiddenField
    id="latitude"
    schema={schema.latitude}
    bind:value={entity.latitude}
  />
{/key}
