<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import DaysGrid from "../../inputs/opening-hours/days-grid.svelte";

  interface Props {
    id: string;
    value: string;
    disabled?: boolean;
    readonly?: any;
    // Proxy vers le FieldWrapper
    description?: string;
    hidden?: boolean;
    hideLabel?: boolean;
    vertical?: boolean;
  }

  let {
    id,
    value = $bindable(),
    disabled = false,
    readonly = undefined,
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
    descriptionText={description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    readonly={readonly ?? $currentSchema?.[id]?.readonly}
  >
    {#snippet children({ onChange })}
      <DaysGrid bind:value onchange={onChange} />
    {/snippet}
  </FieldWrapper>
{/if}
