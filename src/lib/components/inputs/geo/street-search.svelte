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

  const context = getContext<ValidationContext>(contextValidationKey);

  function handleBlur(evt) {
    if (context) context.onBlur(evt);
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
