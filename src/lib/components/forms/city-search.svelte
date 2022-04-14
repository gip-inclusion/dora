<script>
  import { getContext } from "svelte";

  import { contextValidationKey } from "$lib/validation";
  import { getDepartmentFromCityCode } from "$lib/utils";
  import Select from "$lib/components/forms/select.svelte";
  import Button from "$lib/components/button.svelte";
  import { pinDistanceIcon } from "$lib/icons";

  export let handleChange;
  export let placeholder;
  export let disabled = false;
  export let name;
  export let value = undefined;
  export let initialValue = undefined;

  let choices = [];

  const banAPIUrl = "https://api-adresse.data.gouv.fr/";

  async function searchCity(q) {
    const url = `${banAPIUrl}search/?q=${encodeURIComponent(
      q
    )}&limit=10&type=municipality`;
    const response = await fetch(url);
    const jsonResponse = await response.json();
    const results = jsonResponse.features.map((feature) => ({
      value: feature,
      label: `${feature.properties.label} (${getDepartmentFromCityCode(
        feature.properties.postcode
      )})`,
    }));

    return results;
  }

  const context = getContext(contextValidationKey);

  function handleBlur(evt) {
    if (context) context.onBlur(evt);
  }

  const geolocLabelInit = "À proximité";
  let geolocLabel = geolocLabelInit;

  async function searchCityFromLocationSuccess(position) {
    const longitude = position.coords.longitude;
    const latitude = position.coords.latitude;

    // pour tester l'API, décommenter:
    // const q = `lon=2.37&lat=48.357`;
    const q = `lon=${encodeURIComponent(longitude)}&lat=${encodeURIComponent(
      latitude
    )}`;

    const url = `${banAPIUrl}reverse/?${q}`;
    const response = await fetch(url);
    const jsonResponse = await response.json();
    const result = jsonResponse.features.map((feature) => ({
      value: feature,
    }))[0];

    geolocLabel = geolocLabelInit;

    if (result) {
      const label = `${
        result.value.properties.city
      } (${getDepartmentFromCityCode(result.value.properties.postcode)})`;

      result.value.properties.label = result.value.properties.city;
      choices = [
        {
          label,
          value: result.value,
        },
      ];
      value = result.value;
    }
  }

  function searchCityFromLocationError() {
    geolocLabel = "Impossible de trouver votre position";
  }

  async function searchCityFromLocation() {
    if (!navigator.geolocation) {
      geolocLabel = "La géolocalisation n'est pas supportée";
    } else {
      geolocLabel = "Recherche…";
      navigator.geolocation.getCurrentPosition(
        searchCityFromLocationSuccess,
        searchCityFromLocationError
      );
    }
  }
</script>

<Select
  bind:value
  on:blur={handleBlur}
  {name}
  onChange={handleChange}
  {initialValue}
  {placeholder}
  {disabled}
  {choices}
  hideArrow
  searchFunction={searchCity}
  delay="200"
  localFiltering={false}
  minCharactersToSearch="3"
>
  <Button
    slot="prepend"
    label={geolocLabel}
    wFull
    noBackground
    icon={pinDistanceIcon}
    on:click={searchCityFromLocation}
  />
</Select>
