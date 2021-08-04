<script>
  import Select from "$lib/components/forms/select.svelte";

  export let handleChange;
  export let selectedCity;
  export let disabled;

  const banAPIUrl = "https://api-adresse.data.gouv.fr/search/";

  async function searchCity(q) {
    const url = `${banAPIUrl}?q=${encodeURIComponent(
      q
    )}&limit=10&type=municipality`;
    const response = await fetch(url);
    const jsonResponse = await response.json();
    let results = jsonResponse.features.map((feature) => ({
      value: feature,
      label: `${feature.properties.label} (${feature.properties.postcode})`,
    }));
    return results;
  }
</script>

<Select
  onChange={handleChange}
  {disabled}
  placeholder="Commune"
  hideArrow
  searchFunction={searchCity}
  delay="200"
  labelFieldName="label"
  valueFieldName="siret"
  selectedItem={selectedCity}
  localSearch={false}
  minCharactersToSearch="3"
  localFiltering={false} />
