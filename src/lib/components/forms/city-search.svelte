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

  const banAPIUrl = "https://api-adresse.data.gouv.fr/search/";

  async function searchCity(q, reverse) {
    const url = `${banAPIUrl}${
      reverse ? "reverse/" : ""
    }?q=${encodeURIComponent(q)}&limit=10&type=municipality`;
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

  let geolocLabel = "À proximité";

  async function searchCityFromLocationSuccess(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    geolocLabel = `Lat: ${latitude} °, Long: ${longitude} °`;

    const q = `lon=${longitude}&Lat=${latitude}`;

    const res = await searchCity(q, true);

    console.log(res);
  }

  function searchCityFromLocationError() {
    geolocLabel = "Impossible de trouver votre position";
  }

  async function searchCityFromLocation() {
    if (!navigator.geolocation) {
      geolocLabel =
        "La géolocalisation n'est pas supportée par votre navigateur";
    } else {
      geolocLabel = "Recherche de votre position…";
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
  hideArrow
  searchFunction={searchCity}
  delay="200"
  localFiltering={false}
  minCharactersToSearch="3"
>
  <div slot="prepend">
    <Button
      label={geolocLabel}
      iconOnLeftF
      wFull
      noBackground
      icon={pinDistanceIcon}
      on:click={searchCityFromLocation}
    />
  </div>
</Select>
