<script>
  import Select from "$lib/components/forms/select.svelte";

  export let handleChange;
  export let placeholder;
  export let cityCode;
  export let disabled;
  export let value = undefined;
  export let initialValue = undefined;
  const banAPIUrl = "https://api-adresse.data.gouv.fr/search/";

  async function searchAddress(q) {
    const url = `${banAPIUrl}?q=${encodeURIComponent(
      q
    )}&limit=10&citycode=${cityCode}&type=street&type=housenumber`;
    const response = await fetch(url);
    const jsonResponse = await response.json();
    const results = jsonResponse.features.map((feature) => ({
      value: feature,
      label: feature.properties.name,
    }));
    return results;
  }
</script>

<Select
  on:blur
  bind:value
  onChange={handleChange}
  {initialValue}
  {placeholder}
  {disabled}
  hideArrow
  searchFunction={searchAddress}
  delay="200"
  localFiltering={false}
  minCharactersToSearch="3" />
