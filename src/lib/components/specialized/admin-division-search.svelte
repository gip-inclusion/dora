<script lang="ts">
  import Select from "$lib/components/inputs/select/select.svelte";
  import { getApiURL } from "$lib/utils/api";
  import { getDepartmentFromCityCode } from "$lib/utils/misc";
  import {
    contextValidationKey,
    type ValidationContext,
  } from "$lib/validation/validation";
  import { getContext } from "svelte";

  export let id: string;
  export let onChange;
  export let placeholder = null;
  export let disabled = false;
  export let value = undefined;
  export let initialValue = undefined;
  export let readonly = false;
  export let choices = [];
  export let searchType;

  async function searchAdminDivision(q) {
    const url = `${getApiURL()}/admin-division-search/?type=${searchType}&q=${encodeURIComponent(
      q
    )}`;
    const response = await fetch(url);
    const jsonResponse = await response.json();
    const results = jsonResponse.map((result) => ({
      value: result.code,
      label: `${result.name} (${
        searchType === "city"
          ? getDepartmentFromCityCode(result.code)
          : result.code
      })`,
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
  bind:choices
  bind:value
  on:blur={handleBlur}
  {onChange}
  {initialValue}
  {placeholder}
  {readonly}
  {disabled}
  hideArrow
  searchFunction={searchAdminDivision}
  delay="200"
  localFiltering={false}
/>
