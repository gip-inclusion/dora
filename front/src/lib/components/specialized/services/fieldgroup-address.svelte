<script lang="ts">
  import FieldGroup from "$lib/components/display/field-group.svelte";
  import AddressSearchField from "$lib/components/forms/fields/address-search-field.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import CitySearchField from "$lib/components/forms/fields/city-search-field.svelte";
  import HiddenField from "$lib/components/forms/fields/hidden-field.svelte";
  import type { GeoApiValue, Service, Structure } from "$lib/types";
  import { randomId } from "$lib/utils/random";
  import UseStructureInfoButton from "./use-structure-info-button.svelte";

  interface Props {
    entity: Service | Structure;
    parent?: Structure | null;
  }

  let { entity = $bindable(), parent = null }: Props = $props();

  let key = $state(randomId());

  function handleAddressChange(address) {
    const props = address?.properties;
    const coords = address?.geometry.coordinates;
    const lat = coords?.[1];
    const lon = coords?.[0];
    entity.address1 = props?.name;
    entity.postalCode = props?.postcode;
    entity.longitude = lon;
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

      // force la mise à jour du bloc adresse
      key = randomId();
    }
  }

  function handleCityChange(city: GeoApiValue) {
    entity.city = city?.name;
    entity.cityCode = city?.code;
  }
</script>

<FieldGroup title="Lieu d’accueil">
  {#key key}
    <div class="flex flex-col">
      {#if parent}
        <div class="mb-s8 lg:w-2/3 lg:self-end">
          <UseStructureInfoButton
            onclick={fillAddress}
            label="les coordonnées"
          />
        </div>
      {/if}
      <AddressSearchField
        id="address1"
        initialValue={entity.address1}
        onChange={handleAddressChange}
        cityCode={entity.cityCode}
        disabled={!entity.cityCode}
      />
    </div>

    <BasicInputField
      id="address2"
      bind:value={entity.address2}
      descriptionText="Indication : bâtiment, immeuble, étage, numéro d’appartement, etc."
    />

    <BasicInputField
      id="postalCode"
      descriptionText="Format attendu : 5 chiffres. Par exemple : 75000."
      bind:value={entity.postalCode}
    />

    <CitySearchField
      id="city"
      initialValue={entity.city}
      onChange={handleCityChange}
    />

    <HiddenField id="cityCode" value={entity.cityCode} />

    <HiddenField id="longitude" value={entity.longitude} />

    <HiddenField id="latitude" value={entity.latitude} />
  {/key}
</FieldGroup>
