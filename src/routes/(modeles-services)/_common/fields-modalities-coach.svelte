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

  import { orderedCoachOrientationModeValues } from "./modalities-order";

  export let id: string;
  export let service: Service;
  export let servicesOptions: ServicesOptions;

  let coachOrientationModesFocusValue: string | undefined = undefined;
  let preventUpdateExternalFormFields = true;

  function updateExternalFormFields(text: string) {
    if (preventUpdateExternalFormFields) {
      // Pas de réinitialisation des champs au premier chargement
      preventUpdateExternalFormFields = false;
      return;
    }
    service.coachOrientationModesExternalFormLink = "";
    service.coachOrientationModesExternalFormLinkText = text;
  }

  $: externalFormToggle = service.coachOrientationModes.includes(
    "completer-le-formulaire-dadhesion"
  );
  $: {
    updateExternalFormFields(
      externalFormToggle ? "Orienter votre bénéficiaire" : ""
    );
  }

  $: servicesOptions.coachOrientationModes.sort(
    (a, b) =>
      orderedCoachOrientationModeValues[a.value] -
      orderedCoachOrientationModeValues[b.value]
  );
</script>

{#if $currentSchema && "coachOrientationModes" in $currentSchema}
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
      {#each servicesOptions.coachOrientationModes as choice}
        {#if choice.value === "completer-le-formulaire-dadhesion" && service.coachOrientationModes.includes("completer-le-formulaire-dadhesion")}
          <Checkbox
            name={id}
            bind:group={service.coachOrientationModes}
            label={choice.label}
            value={choice.value}
            readonly={$currentSchema?.[id]?.readonly}
            errorMessage={formatErrors(id, errorMessages)}
            focused={coachOrientationModesFocusValue === choice.value}
            on:change={onChange}
            on:focus={() => (coachOrientationModesFocusValue = choice.value)}
            on:blur={() => (coachOrientationModesFocusValue = undefined)}
          >
            <BasicInputField
              id="coachOrientationModesExternalFormLinkText"
              description="Par exemple : Orienter votre bénéficiaire, Faire une simulation, Prendre rendez-vous, etc."
              vertical
              bind:value={service.coachOrientationModesExternalFormLinkText}
            />
            <BasicInputField
              id="coachOrientationModesExternalFormLink"
              description="Lien vers votre formulaire ou plateforme. Format attendu : https://exemple.fr"
              type="url"
              vertical
              bind:value={service.coachOrientationModesExternalFormLink}
            />
          </Checkbox>
        {:else if choice.value === "autre" && service.coachOrientationModes.includes("autre")}
          <Checkbox
            name={id}
            bind:group={service.coachOrientationModes}
            label={choice.label}
            value={choice.value}
            readonly={$currentSchema?.[id]?.readonly}
            errorMessage={formatErrors(id, errorMessages)}
            focused={coachOrientationModesFocusValue === choice.value}
            on:change={onChange}
            on:focus={() => (coachOrientationModesFocusValue = choice.value)}
            on:blur={() => (coachOrientationModesFocusValue = undefined)}
          >
            <BasicInputField
              id="coachOrientationModesOther"
              hideLabel
              vertical
              bind:value={service.coachOrientationModesOther}
            />
          </Checkbox>
        {:else}
          <Checkbox
            name={id}
            bind:group={service.coachOrientationModes}
            label={choice.label}
            value={choice.value}
            readonly={$currentSchema?.[id]?.readonly}
            errorMessage={formatErrors(id, errorMessages)}
            focused={coachOrientationModesFocusValue === choice.value}
            on:change={onChange}
            on:focus={() => (coachOrientationModesFocusValue = choice.value)}
            on:blur={() => (coachOrientationModesFocusValue = undefined)}
          />
        {/if}
      {/each}
    </div>
  </FieldWrapper>
{/if}
