<script>
  import Select from "$lib/components/forms/select.svelte";

  export let handleChange;
  export let placeholder;
  export let disabled = false;
  export let selectedItem = null;

  const banAPIUrl = "https://api-adresse.data.gouv.fr/search/";

  async function searchCity(q) {
    const url = `${banAPIUrl}?q=${encodeURIComponent(
      q
    )}&limit=10&type=municipality`;
    const response = await fetch(url);
    const jsonResponse = await response.json();
    const results = jsonResponse.features.map((feature) => ({
      value: feature,
      label: `${feature.properties.label} (${feature.properties.postcode})`,
    }));
    return results;
  }
</script>

<Select
  on:blur
  bind:selectedItem
  onChange={handleChange}
  {placeholder}
  {disabled}
  hideArrow
  searchFunction={searchCity}
  delay="200"
  labelFieldName="label"
  localFiltering={false}
  minCharactersToSearch="3" />
