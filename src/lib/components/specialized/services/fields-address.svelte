<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import AddressSearchField from "$lib/components/forms/fields/address-search-field.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import CitySearchField from "$lib/components/forms/fields/city-search-field.svelte";
  import HiddenField from "$lib/components/forms/fields/hidden-field.svelte";
  import { syncIcon } from "$lib/icons";
  import type { GeoApiValue, Service, Structure } from "$lib/types";

  export let entity: Service | Structure;
  export let parent: Structure | null = null;

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

  function fillAddress() {
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

  function handleCityChange(city: GeoApiValue) {
    entity.city = city?.name;
    entity.cityCode = city?.code;
  }
</script>

{#key entity.slug}
  <div class="flex flex-col">
    {#if parent}
      <div class="mb-s8 lg:w-2/3 lg:self-end">
        <Button
          on:click={fillAddress}
          icon={syncIcon}
          noBackground
          small
          noPadding
          label="Utiliser les coordonnées de la structure"
        />
      </div>
    {/if}
    <CitySearchField
      id="city"
      initialValue={entity.city}
      onChange={handleCityChange}
      placeholder="Saisissez et validez votre ville"
    />
  </div>
  <AddressSearchField
    id="address1"
    initialValue={entity.address1}
    onChange={handleAddressChange}
    cityCode={entity.cityCode}
    placeholder="3 rue du parc"
    disabled={!entity.cityCode}
  />

  <BasicInputField
    id="address2"
    bind:value={entity.address2}
    placeholder="batiment, escalier, etc."
  />

  <BasicInputField
    id="postalCode"
    bind:value={entity.postalCode}
    placeholder="00000"
  />

  <HiddenField id="cityCode" value={entity.cityCode} />

  <HiddenField id="longitude" value={entity.longitude} />

  <HiddenField id="latitude" value={entity.latitude} />
{/key}
