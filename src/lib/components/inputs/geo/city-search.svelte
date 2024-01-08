<script lang="ts">
  import Select from "$lib/components/inputs/select/select.svelte";
  import { pinDistanceIcon } from "$lib/icons";
  import type { Choice, GeoApiValue } from "$lib/types";
  import { getApiURL } from "$lib/utils/api";
  import { fetchData, getDepartmentFromCityCode } from "$lib/utils/misc";

  export let onChange: (newValue: GeoApiValue) => void;

  export let placeholder;
  export let disabled = false;
  export let id;
  export let value = undefined;
  export let initialValue: string | undefined = undefined;

  let choices: Choice[] = [];
  async function searchCity(query) {
    const url = `${getApiURL()}/admin-division-search/?type=city&q=${encodeURIComponent(
      query
    )}`;

    const response = await fetch(url);
    const jsonResponse = await response.json();
    const results = jsonResponse.map((result) => ({
      value: result,
      label: `${result.name} (${getDepartmentFromCityCode(result.code)})`,
    }));

    return results;
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

    const response = await fetchData<GeoApiValue>(url);
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

  function searchCityFromLocation() {
    if (!navigator.geolocation) {
      geolocLabel = "La géolocalisation n’est pas supportée";
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
  on:blur
  {id}
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
      class="flex w-full border-gray-02 px-s8 py-s12 text-f14 text-gray-text"
      on:click|preventDefault|stopPropagation={searchCityFromLocation}
      class:border-b={results?.length}
    >
      <span class="mr-s8 h-s24 w-s24 fill-current">
        {@html pinDistanceIcon}
      </span>

      {geolocLabel}
    </button>
  </div>
</Select>
