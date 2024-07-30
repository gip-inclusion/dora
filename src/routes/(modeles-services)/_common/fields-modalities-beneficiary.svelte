<script lang="ts">
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

  import { orderedBeneficiariesAccessModeValues } from "./modalities-order";

  export let id: string;
  export let service: Service;
  export let servicesOptions: ServicesOptions;

  let beneficiariesAccessModesFocusValue: string | undefined = undefined;

  $: {
    // Suppression du lien vers le formulaire externe et de son intitulé
    // lorsque la case du formulaire externe est décochée.
    if (
      !service.beneficiariesAccessModes.includes(
        "completer-le-formulaire-dadhesion"
      )
    ) {
      service.beneficiariesAccessModesExternalFormLink = "";
      service.beneficiariesAccessModesExternalFormLinkText = "";
    }
  }

  $: servicesOptions.beneficiariesAccessModes.sort(
    (a, b) =>
      orderedBeneficiariesAccessModeValues[a.value] -
      orderedBeneficiariesAccessModeValues[b.value]
  );
</script>

{#if $currentSchema && "beneficiariesAccessModes" in $currentSchema}
  <FieldWrapper
    {id}
    let:onChange
    let:errorMessages
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    description="Plusieurs choix possibles."
    readonly={$currentSchema?.[id]?.readonly}
  >
    <div class="flex flex-col gap-s8">
      {#each servicesOptions.beneficiariesAccessModes as choice}
        {#if choice.value === "completer-le-formulaire-dadhesion" && service.beneficiariesAccessModes.includes("completer-le-formulaire-dadhesion")}
          <Checkbox
            name={id}
            bind:group={service.beneficiariesAccessModes}
            label={choice.label}
            value={choice.value}
            readonly={$currentSchema?.[id]?.readonly}
            errorMessage={formatErrors(id, errorMessages)}
            focused={beneficiariesAccessModesFocusValue === choice.value}
            on:change={onChange}
            on:focus={() => (beneficiariesAccessModesFocusValue = choice.value)}
            on:blur={() => (beneficiariesAccessModesFocusValue = undefined)}
          >
            <BasicInputField
              id="beneficiariesAccessModesExternalFormLinkText"
              description="Par exemple : Faire une demande, Faire une simulation, Prendre rendez-vous, etc."
              placeholder="Faire une demande"
              vertical
              bind:value={service.beneficiariesAccessModesExternalFormLinkText}
            />
            <BasicInputField
              id="beneficiariesAccessModesExternalFormLink"
              description="Lien vers votre formulaire ou plateforme. Format attendu : https://exemple.fr"
              type="url"
              vertical
              bind:value={service.beneficiariesAccessModesExternalFormLink}
            />
          </Checkbox>
        {:else if choice.value === "autre" && service.beneficiariesAccessModes.includes("autre")}
          <Checkbox
            name={id}
            bind:group={service.beneficiariesAccessModes}
            label={choice.label}
            value={choice.value}
            readonly={$currentSchema?.[id]?.readonly}
            errorMessage={formatErrors(id, errorMessages)}
            focused={beneficiariesAccessModesFocusValue === choice.value}
            on:change={onChange}
            on:focus={() => (beneficiariesAccessModesFocusValue = choice.value)}
            on:blur={() => (beneficiariesAccessModesFocusValue = undefined)}
          >
            <BasicInputField
              id="beneficiariesAccessModesOther"
              hideLabel
              vertical
              bind:value={service.beneficiariesAccessModesOther}
            />
          </Checkbox>
        {:else}
          <Checkbox
            name={id}
            bind:group={service.beneficiariesAccessModes}
            label={choice.label}
            value={choice.value}
            readonly={$currentSchema?.[id]?.readonly}
            errorMessage={formatErrors(id, errorMessages)}
            focused={beneficiariesAccessModesFocusValue === choice.value}
            on:change={onChange}
            on:focus={() => (beneficiariesAccessModesFocusValue = choice.value)}
            on:blur={() => (beneficiariesAccessModesFocusValue = undefined)}
          />
        {/if}
      {/each}
    </div>
  </FieldWrapper>
{/if}
