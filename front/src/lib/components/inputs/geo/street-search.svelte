<script lang="ts">
  import Select from "$lib/components/inputs/select/select.svelte";
  import {
    contextValidationKey,
    type ValidationContext,
  } from "$lib/validation/validation";
  import { getContext } from "svelte";

  interface Props {
    id: string;
    onChange: (newValue: string) => void;
    placeholder: string;
    cityCode: string;
    disabled: boolean;
    value?: string;
    initialValue?: string;
    readonly?: boolean;
  }

  let {
    id,
    onChange,
    placeholder,
    cityCode,
    disabled,
    value = $bindable(),
    initialValue,
    readonly = false,
  }: Props = $props();

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
  onblur={handleBlur}
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
