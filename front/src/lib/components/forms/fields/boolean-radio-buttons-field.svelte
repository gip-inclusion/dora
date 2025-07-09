<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import RadioButtons from "../../inputs/radio-buttons.svelte";

  // Laisser la valeur par défault ici. Si la valeur entrante est undefined ou null

  const choices = [
    { value: true, label: yesLabel },
    { value: false, label: noLabel },
  ];

  interface Props {
    id: string;
    // on veut la considérer comme false;
    value?: boolean;
    disabled?: boolean;
    readonly?: any;
    // Spécifiques
    yesLabel?: string;
    noLabel?: string;
    // Proxy vers le FieldWrapper
    description?: string;
    hidden?: boolean;
    hideLabel?: boolean;
    vertical?: boolean;
  }

  let {
    id,
    value = $bindable(false),
    disabled = false,
    readonly = $currentSchema?.[id]?.readonly,
    yesLabel = "Oui",
    noLabel = "Non",
    description = "",
    hidden = false,
    hideLabel = false,
    vertical = false,
  }: Props = $props();
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    {readonly}
  >
    {#snippet children({ errorMessages })}
      <RadioButtons
        {id}
        name={id}
        bind:group={value}
        on:change
        {choices}
        {disabled}
        {readonly}
        {errorMessages}
      />
    {/snippet}
  </FieldWrapper>
{/if}
