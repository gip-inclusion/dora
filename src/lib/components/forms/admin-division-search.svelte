<script lang="ts">
  import Select from "$lib/components/forms/select.svelte";
  import { getDepartmentFromCityCode } from "$lib/utils";
  import { getApiURL } from "$lib/utils/api";
  import {
    contextValidationKey,
    type ValidationContext,
  } from "$lib/validation";
  import { getContext } from "svelte";

  export let handleChange;
  export let placeholder = null;
  export let disabled = false;
  export let name;
  export let value = undefined;
  export let initialValue = undefined;
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
  bind:choices
  bind:value
  on:blur={handleBlur}
  {name}
  onChange={handleChange}
  {initialValue}
  {placeholder}
  {disabled}
  hideArrow
  searchFunction={searchAdminDivision}
  delay="200"
  localFiltering={false}
/>
