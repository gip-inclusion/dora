<script>
  import { getContext } from "svelte";

  import { contextValidationKey } from "$lib/validation";
  import { getDepartmentFromCityCode } from "$lib/utils";
  import Select from "$lib/components/forms/select.svelte";
  import Button from "$lib/components/button.svelte";

  export let handleChange;
  export let placeholder;
  export let disabled = false;
  export let name;
  export let value = undefined;
  export let initialValue = undefined;

  const banAPIUrl = "https://api-adresse.data.gouv.fr/search/";

  async function searchCity(q) {
    const url = `${banAPIUrl}?q=${encodeURIComponent(
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

  let geolocLabel = "À proximité";

  function geoFindMe() {
    function success(position) {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;
      geolocLabel = `Lat: ${latitude} °, Long: ${longitude} °`;
    }

    function error() {
      geolocLabel = "Unable to retrieve your location";
    }

    if (!navigator.geolocation) {
      geolocLabel = "Geolocation is not supported by your browser";
    } else {
      geolocLabel = "Locating…";
      navigator.geolocation.getCurrentPosition(success, error);
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
      small
      iconOnLeft
      tertiary
      wFull
      on:click={geoFindMe}
    />
  </div>
</Select>
