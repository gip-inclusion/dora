<script lang="ts">
  import { untrack } from "svelte";

  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import Checkbox from "$lib/components/inputs/checkbox.svelte";
  import type { Service, ServicesOptions } from "$lib/types";
  import {
    currentFormData,
    currentSchema,
    formatErrors,
    isRequired,
  } from "$lib/validation/validation";

  import { orderedModesMobilisationValues } from "./modalities-order";

  interface Props {
    id: string;
    service: Service;
    servicesOptions: ServicesOptions;
  }

  let { id, service = $bindable(), servicesOptions }: Props = $props();

  let modesMobilisationFocusValue: string | undefined = $state();

  let externalFormToggle = $derived(
    service.modesMobilisation.includes("utiliser-lien-mobilisation")
  );

  $effect(() => {
    if (!externalFormToggle) {
      untrack(() => {
        service.lienMobilisation = "";
      });
    }
  });

  const sortedModesMobilisation = $derived(
    servicesOptions.modesMobilisation.toSorted(
      (a, b) =>
        orderedModesMobilisationValues[a.value] -
        orderedModesMobilisationValues[b.value]
    )
  );
</script>

{#if $currentSchema && "modesMobilisation" in $currentSchema}
  <FieldWrapper
    {id}
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    descriptionText="Plusieurs choix possibles."
    readonly={$currentSchema?.[id]?.readonly}
  >
    {#snippet children({ onChange, errorMessages })}
      <div class="gap-s8 flex flex-col">
        {#each sortedModesMobilisation as choice}
          {#if choice.value === "utiliser-lien-mobilisation" && externalFormToggle}
            <Checkbox
              name={id}
              bind:group={service.modesMobilisation}
              label={choice.label}
              value={choice.value}
              readonly={$currentSchema?.[id]?.readonly}
              errorMessage={formatErrors(id, errorMessages)}
              focused={modesMobilisationFocusValue === choice.value}
              onchange={onChange}
              onfocus={() => (modesMobilisationFocusValue = choice.value)}
              onblur={() => (modesMobilisationFocusValue = undefined)}
            >
              <BasicInputField
                id="lienMobilisation"
                descriptionText="Lien vers votre formulaire ou plateforme. Format attendu : https://exemple.fr"
                type="url"
                vertical
                bind:value={service.lienMobilisation}
              />
            </Checkbox>
          {:else}
            <Checkbox
              name={id}
              bind:group={service.modesMobilisation}
              label={choice.label}
              value={choice.value}
              readonly={$currentSchema?.[id]?.readonly}
              errorMessage={formatErrors(id, errorMessages)}
              focused={modesMobilisationFocusValue === choice.value}
              onchange={onChange}
              onfocus={() => (modesMobilisationFocusValue = choice.value)}
              onblur={() => (modesMobilisationFocusValue = undefined)}
            />
          {/if}
        {/each}
      </div>
    {/snippet}
  </FieldWrapper>
{/if}
