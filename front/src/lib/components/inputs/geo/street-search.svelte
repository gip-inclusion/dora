<script lang="ts">
  import { getContext } from "svelte";

  import * as Sentry from "@sentry/sveltekit";

  import Select from "$lib/components/inputs/select/select.svelte";

  import { fetchWithRetry } from "$lib/utils/fetch-retry";

  import {
    contextValidationKey,
    type ValidationContext,
  } from "$lib/validation/validation";

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

  async function searchAddress(query: string) {
    const url = `${banAPIUrl}?q=${encodeURIComponent(
      query
    )}&limit=10&citycode=${cityCode}`;

    try {
      const response = await fetchWithRetry(url, undefined, {
        maxAttempts: 3,
      });

      if (!response.ok) {
        return [];
      }

      const jsonResponse = await response.json();
      const results = jsonResponse.features
        .filter((feature) => feature.properties.type !== "municipality")
        .map((feature) => ({
          value: feature,
          label: feature.properties.name,
        }));
      return results;
    } catch (error) {
      Sentry.captureException(error);
      return [];
    }
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
  delay={200}
  localFiltering={false}
  minCharactersToSearch={3}
  {readonly}
/>
