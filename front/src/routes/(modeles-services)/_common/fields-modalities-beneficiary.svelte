<script lang="ts">
  import { run } from "svelte/legacy";

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

  interface Props {
    id: string;
    service: Service;
    servicesOptions: ServicesOptions;
  }

  let { id, service = $bindable(), servicesOptions }: Props = $props();

  let beneficiariesAccessModesFocusValue: string | undefined =
    $state(undefined);
  let preventUpdateExternalFormFields = true;

  function updateExternalFormFields(text: string) {
    if (preventUpdateExternalFormFields) {
      // Pas de réinitialisation des champs au premier chargement
      preventUpdateExternalFormFields = false;
      return;
    }
    service.beneficiariesAccessModesExternalFormLink = "";
    service.beneficiariesAccessModesExternalFormLinkText = text;
  }

  let externalFormToggle = $derived(
    service.beneficiariesAccessModes.includes(
      "completer-le-formulaire-dadhesion"
    )
  );
  run(() => {
    updateExternalFormFields(externalFormToggle ? "Faire une demande" : "");
  });

  run(() => {
    servicesOptions.beneficiariesAccessModes.sort(
      (a, b) =>
        orderedBeneficiariesAccessModeValues[a.value] -
        orderedBeneficiariesAccessModeValues[b.value]
    );
  });
</script>

{#if $currentSchema && "beneficiariesAccessModes" in $currentSchema}
  <FieldWrapper
    {id}
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    descriptionText="Plusieurs choix possibles."
    readonly={$currentSchema?.[id]?.readonly}
  >
    {#snippet children({ onChange, errorMessages })}
      <div class="gap-s8 flex flex-col">
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
              on:focus={() =>
                (beneficiariesAccessModesFocusValue = choice.value)}
              on:blur={() => (beneficiariesAccessModesFocusValue = undefined)}
            >
              <BasicInputField
                id="beneficiariesAccessModesExternalFormLinkText"
                descriptionText="Par exemple : Faire une demande, Faire une simulation, Prendre rendez-vous, etc."
                vertical
                bind:value={
                  service.beneficiariesAccessModesExternalFormLinkText
                }
              />
              <BasicInputField
                id="beneficiariesAccessModesExternalFormLink"
                descriptionText="Lien vers votre formulaire ou plateforme. Format attendu : https://exemple.fr"
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
              on:focus={() =>
                (beneficiariesAccessModesFocusValue = choice.value)}
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
              on:focus={() =>
                (beneficiariesAccessModesFocusValue = choice.value)}
              on:blur={() => (beneficiariesAccessModesFocusValue = undefined)}
            />
          {/if}
        {/each}
      </div>
    {/snippet}
  </FieldWrapper>
{/if}
