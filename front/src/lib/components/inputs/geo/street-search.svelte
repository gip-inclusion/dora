<script lang="ts">
  import Select from "$lib/components/inputs/select/select.svelte";
  import {
    contextValidationKey,
    type ValidationContext,
  } from "$lib/validation/validation";
  import { getContext } from "svelte";

  export let id: string;
  export let onChange: (newValue: string) => void;
  export let placeholder: string;
  export let cityCode: string;
  export let disabled: boolean;
  export let value: string | undefined = undefined;
  export let initialValue: string | undefined = undefined;
  export let readonly = false;

  const banAPIUrl = "https://api-adresse.data.gouv.fr/search/";

  async function searchAddress(query) {
    const url = `${banAPIUrl}?q=${encodeURIComponent(
      query
    )}&limit=10&citycode=${cityCode}`;
    const response = await fetch(url);
    const jsonResponse = await response.json();
    const results = jsonResponse.features
      .filter((feature) => feature.properties.type !== "municipality")
      .map((feature) => ({
        value: feature,
        label: feature.properties.name,
      }));
    return results;
  }

  const context = getContext<ValidationContext>(contextValidationKey);

  function handleBlur(evt) {
    if (context) {
      context.onBlur(evt);
    }
  }
</script>

<Select
  {id}
  bind:value
  on:blur={handleBlur}
  {onChange}
  {initialValue}
  {placeholder}
  {disabled}
  hideArrow
  searchFunction={searchAddress}
  delay="200"
  localFiltering={false}
  minCharactersToSearch="3"
  {readonly}
/>
