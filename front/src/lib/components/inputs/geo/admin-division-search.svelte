<script lang="ts">
  import Select from "$lib/components/inputs/select/select.svelte";
  import type { AdminDivisionType, GeoApiValue } from "$lib/types";
  import { getApiURL } from "$lib/utils/api";
  import { getDepartmentFromCityCode } from "$lib/utils/misc";
  import {
    contextValidationKey,
    type ValidationContext,
  } from "$lib/validation/validation";
  import { getContext } from "svelte";

  interface Props {
    id: string;
    onChange: (adminDetails: GeoApiValue) => void;
    placeholder?: string;
    disabled?: boolean;
    value?: GeoApiValue;
    initialValue?: GeoApiValue;
    readonly?: boolean;
    choices?: any;
    searchType: AdminDivisionType;
  }

  let {
    id,
    onChange,
    placeholder = "",
    disabled = false,
    value = $bindable(),
    initialValue,
    readonly = false,
    choices = $bindable([]),
    searchType,
  }: Props = $props();

  async function searchAdminDivision(query) {
    const url = new URL("/admin-division-search/", getApiURL());
    url.searchParams.set("type", searchType);
    url.searchParams.set("q", query);
    const response = await fetch(url);
    const jsonResponse = await response.json();
    const results = jsonResponse.map((result) => {
      let label = result.name;
      if (searchType === "city") {
        label += ` (${getDepartmentFromCityCode(result.code)})`;
      } else if (searchType !== "region") {
        label += ` (${result.code})`;
      }

      return {
        value: result,
        label,
      };
    });

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
  bind:choices
  bind:value
  onblur={handleBlur}
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
