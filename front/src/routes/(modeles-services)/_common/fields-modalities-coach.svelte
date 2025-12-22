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

  import { orderedCoachOrientationModeValues } from "./modalities-order";

  interface Props {
    id: string;
    service: Service;
    servicesOptions: ServicesOptions;
  }

  let { id, service = $bindable(), servicesOptions }: Props = $props();

  let coachOrientationModesFocusValue: string | undefined = $state();

  let externalFormToggle = $derived(
    service.coachOrientationModes.includes("completer-le-formulaire-dadhesion")
  );

  $effect(() => {
    if (!externalFormToggle) {
      untrack(() => {
        service.coachOrientationModesExternalFormLink = "";
        service.coachOrientationModesExternalFormLinkText =
          "Orienter votre bénéficiaire";
      });
    }
  });

  const sortedCoachOrientationModes = $derived(
    servicesOptions.coachOrientationModes.toSorted(
      (a, b) =>
        orderedCoachOrientationModeValues[a.value] -
        orderedCoachOrientationModeValues[b.value]
    )
  );
</script>

{#if $currentSchema && "coachOrientationModes" in $currentSchema}
  <FieldWrapper
    {id}
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    descriptionText="Plusieurs choix possibles."
    readonly={$currentSchema?.[id]?.readonly}
  >
    {#snippet children({ onChange, errorMessages })}
      <div class="gap-s8 flex flex-col">
        {#each sortedCoachOrientationModes as choice}
          {#if choice.value === "completer-le-formulaire-dadhesion" && service.coachOrientationModes.includes("completer-le-formulaire-dadhesion")}
            <Checkbox
              name={id}
              bind:group={service.coachOrientationModes}
              label={choice.label}
              value={choice.value}
              readonly={$currentSchema?.[id]?.readonly}
              errorMessage={formatErrors(id, errorMessages)}
              focused={coachOrientationModesFocusValue === choice.value}
              onchange={onChange}
              onfocus={() => (coachOrientationModesFocusValue = choice.value)}
              onblur={() => (coachOrientationModesFocusValue = undefined)}
            >
              <BasicInputField
                id="coachOrientationModesExternalFormLinkText"
                descriptionText="Par exemple : Orienter votre bénéficiaire, Faire une simulation, Prendre rendez-vous, etc."
                vertical
                bind:value={service.coachOrientationModesExternalFormLinkText}
              />
              <BasicInputField
                id="coachOrientationModesExternalFormLink"
                descriptionText="Lien vers votre formulaire ou plateforme. Format attendu : https://exemple.fr"
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
              onchange={onChange}
              onfocus={() => (coachOrientationModesFocusValue = choice.value)}
              onblur={() => (coachOrientationModesFocusValue = undefined)}
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
              onchange={onChange}
              onfocus={() => (coachOrientationModesFocusValue = choice.value)}
              onblur={() => (coachOrientationModesFocusValue = undefined)}
            />
          {/if}
        {/each}
      </div>
    {/snippet}
  </FieldWrapper>
{/if}
