<script lang="ts">
  import { getApiURL } from "$lib/utils/api";
  import CitySearch from "$lib/components/inputs/geo/city-search.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import FieldWrapper from "$lib/components/inputs/field-wrapper.svelte";

  export let establishment;
  export let isOwnStructure = true;

  let city;
  export let onCityChange = null;
  export let onEstablishmentChange = null;

  function handleCityChange(newCity) {
    city = newCity;
    establishment = null;
    if (onCityChange) onCityChange(newCity);
  }

  async function handleEstablishmentChange(newEstablishment) {
    establishment = newEstablishment;
    if (onEstablishmentChange) onEstablishmentChange(newEstablishment);
  }

  async function searchSirene(q) {
    const url = `${getApiURL()}/search-sirene/${
      city.code
    }/?q=${encodeURIComponent(q)}`;

    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });

    const jsonResponse = await response.json();

    const results = jsonResponse.map((result) => {
      result.label = `${result.name} (${result.address1})`;
      return {
        value: result,
        label: result.label,
      };
    });
    return results;
  }

  const structureLabel = isOwnStructure
    ? "Nom de votre structure"
    : "Nom de la structure de votre partenaire";
</script>

<FieldWrapper id="city" label="Commune" required vertical>
  <CitySearch
    id="city"
    onChange={handleCityChange}
    placeholder="Saisissez et sélectionnez le nom de la ville"
  />
</FieldWrapper>

<FieldWrapper id="siret-select" label={structureLabel} required vertical>
  <Select
    id="siret-select"
    onChange={handleEstablishmentChange}
    disabled={!city?.code}
    placeholder="Commencez à saisir et choisissez dans la liste"
    hideArrow
    searchFunction={searchSirene}
    delay="200"
    localFiltering={false}
    postfixValueFunction={(item) => item.siret}
    minCharactersToSearch="3"
  />
</FieldWrapper>
