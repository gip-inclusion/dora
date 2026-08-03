<script lang="ts">
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import Checkbox from "$lib/components/inputs/checkbox.svelte";
  import type { Service, ServicesOptions } from "$lib/types";
  import {
    currentFormData,
    currentSchema,
    formatErrors,
    isRequired,
  } from "$lib/validation/validation";

  import { orderedMobilisableParValues } from "./modalities-order";

  interface Props {
    id: string;
    service: Service;
    servicesOptions: ServicesOptions;
  }

  let { id, service = $bindable(), servicesOptions }: Props = $props();

  let mobilisableParFocusValue: string | undefined = $state();

  const sortedMobilisablePar = $derived(
    servicesOptions.mobilisablePar.toSorted(
      (a, b) =>
        orderedMobilisableParValues[a.value] -
        orderedMobilisableParValues[b.value]
    )
  );
</script>

{#if $currentSchema && "mobilisablePar" in $currentSchema}
  <FieldWrapper
    {id}
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    descriptionText="Plusieurs choix possibles."
    readonly={$currentSchema?.[id]?.readonly}
  >
    {#snippet children({ onChange, errorMessages })}
      <div class="gap-s8 flex flex-col">
        {#each sortedMobilisablePar as choice}
          <Checkbox
            name={id}
            bind:group={service.mobilisablePar}
            label={choice.label}
            value={choice.value}
            readonly={$currentSchema?.[id]?.readonly}
            errorMessage={formatErrors(id, errorMessages)}
            focused={mobilisableParFocusValue === choice.value}
            onchange={onChange}
            onfocus={() => (mobilisableParFocusValue = choice.value)}
            onblur={() => (mobilisableParFocusValue = undefined)}
          />
        {/each}
      </div>
    {/snippet}
  </FieldWrapper>
{/if}
