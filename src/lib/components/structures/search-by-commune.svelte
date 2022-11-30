<script lang="ts">
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Select from "$lib/components/forms/select.svelte";
  import { getApiURL } from "$lib/utils/api";

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

<Field type="custom" label="Commune" required vertical>
  <CitySearch
    slot="custom-input"
    name="city-select"
    placeholder="Saisissez et sélectionnez le nom de la ville"
    onChange={handleCityChange}
  />
</Field>
<Field type="custom" label={structureLabel} required vertical>
  <Select
    slot="custom-input"
    name="siret-select"
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
</Field>
