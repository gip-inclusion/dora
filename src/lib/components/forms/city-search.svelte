<script>
  import { getContext } from "svelte";

  import { contextValidationKey } from "$lib/validation";
  import { fetchData, getDepartmentFromCityCode } from "$lib/utils";
  import { getApiURL } from "$lib/utils/api.js";
  import Select from "$lib/components/forms/select.svelte";
  import { pinDistanceIcon } from "$lib/icons";

  export let onChange;
  export let placeholder;
  export let disabled = false;
  export let name;
  export let value = undefined;
  export let initialValue = undefined;

  let choices = [];
  async function searchCity(q) {
    const url = `${getApiURL()}/admin-division-search/?type=city&q=${encodeURIComponent(
      q
    )}`;

    const response = await fetch(url);
    const jsonResponse = await response.json();
    const results = jsonResponse.map((result) => ({
      value: result,
      label: `${result.name} (${getDepartmentFromCityCode(result.code)})`,
    }));

    return results;
  }

  const context = getContext(contextValidationKey);

  function handleBlur(evt) {
    if (context) context.onBlur(evt);
  }

  const geolocLabelInit = "Autour de moi";
  let geolocLabel = geolocLabelInit;

  function searchCityFromLocationError() {
    geolocLabel = "Position introuvable";
  }

  async function searchCityFromLocationSuccess(position) {
    const longitude = position.coords.longitude;
    const latitude = position.coords.latitude;

    // pour tester l'API, décommenter:
    // const q = `lon=2.37&lat=48.357`;
    const url = `${getApiURL()}/admin-division-reverse-search/?type=city&lon=${encodeURIComponent(
      longitude
    )}&lat=${encodeURIComponent(latitude)}`;

    const response = await fetchData(url);
    if (response.ok) {
      const city = response.data;

      geolocLabel = geolocLabelInit;

      if (city) {
        choices = [
          {
            label: `${city.name} (${getDepartmentFromCityCode(city.code)})`,
            value: city,
          },
        ];
        value = city;
      }
    } else {
      searchCityFromLocationError();
    }
  }

  async function searchCityFromLocation() {
    if (!navigator.geolocation) {
      geolocLabel = "La géolocalisation n'est pas supportée";
    } else {
      geolocLabel = "Recherche";
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
  {onChange}
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
  <div slot="prepend" class="px-s8 pt-s8" let:results>
    <button
      class="flex w-full border-gray-02 py-s12 px-s8 text-f14 text-gray-text"
      on:click|preventDefault|stopPropagation={searchCityFromLocation}
      class:border-b={results?.length}
    >
      <span class="mr-s8 h-s24 w-s24 fill-current ">
        {@html pinDistanceIcon}
      </span>

      {geolocLabel}
    </button>
  </div>
</Select>
