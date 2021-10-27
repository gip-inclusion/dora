<script>
  import { getApiURL } from "$lib/utils/api.js";
  import Select from "$lib/components/forms/select.svelte";

  export let handleChange;
  export let selectedCity;
  export let disabled;
  export let name;
  export let placeholder;

  async function searchSirene(q) {
    const sireneAPIUrl = `${getApiURL()}/search-sirene/${
      selectedCity.properties.citycode
    }/?q=${encodeURIComponent(q)}`;
    const response = await fetch(sireneAPIUrl, {
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
</script>

<Select
  onChange={handleChange}
  {disabled}
  {name}
  {placeholder}
  hideArrow
  searchFunction={searchSirene}
  delay="200"
  localFiltering={false}
  postfixValueFunction={(item) => item.siret}
  minCharactersToSearch="3"
/>
