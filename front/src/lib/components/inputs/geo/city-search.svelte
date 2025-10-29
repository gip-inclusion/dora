<script lang="ts">
  import PinDistanceFillMap from "svelte-remix/PinDistanceFillMap.svelte";

  import Select from "$lib/components/inputs/select/select.svelte";
  import type { Choice, GeoApiValue } from "$lib/types";
  import { customFetch, getApiURL } from "$lib/utils/api";
  import { fetchData, getDepartmentFromCityCode } from "$lib/utils/misc";

  interface Props {
    onblur?: (evt: FocusEvent) => void;
    onChange: (newValue: GeoApiValue) => void;
    disabled?: boolean;
    id: string;
    value?: any;
    initialValue?: string;
  }

  let {
    onblur,
    onChange,
    disabled = false,
    id,
    value = $bindable(),
    initialValue,
  }: Props = $props();

  let choices: Choice[] = $state([]);
  async function searchCity(query) {
    const url = `${getApiURL()}/admin-division-search/?type=city&q=${encodeURIComponent(
      query
    )}`;

    const response = await customFetch(url);
    const jsonResponse = await response.json();
    const results = jsonResponse.map((result) => ({
      value: result,
      label: `${result.name} (${getDepartmentFromCityCode(result.code)})`,
    }));

    return results;
  }

  const geolocLabelInit = "Autour de moi";
  let geolocLabel = $state(geolocLabelInit);

  function searchCityFromLocationError() {
    geolocLabel = "Position introuvable";
  }

  async function searchCityFromLocationSuccess(position) {
    const longitude = position.coords.longitude;
    const latitude = position.coords.latitude;

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

  function handleClickSearchCityFromLocation(event: MouseEvent) {
    event.stopPropagation();
    event.preventDefault();
    searchCityFromLocation();
  }
</script>

<Select
  bind:value
  {onblur}
  {id}
  {onChange}
  {initialValue}
  {disabled}
  {choices}
  hideArrow
  searchFunction={searchCity}
  delay="200"
  localFiltering={false}
  minCharactersToSearch="3"
>
  {#snippet prepend()}
    <div class="px-s8 pt-s8">
      <button
        class="border-gray-02 px-s8 py-s12 text-f14 text-gray-text flex w-full"
        onclick={handleClickSearchCityFromLocation}
      >
        <span class="mr-s8 h-s24 w-s24 fill-current">
          <PinDistanceFillMap />
        </span>

        {geolocLabel}
      </button>
    </div>
  {/snippet}
</Select>
