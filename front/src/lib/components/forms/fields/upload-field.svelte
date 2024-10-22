<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import Uploader from "../../inputs/uploader.svelte";

  export let id: string;
  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;
  export let label = $currentSchema?.[id]?.label;

  // Spécifique
  export let fileKeys: string[];
  export let structureSlug: string | undefined = undefined;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;
  export let dynamicId = false;
</script>

{#if $currentSchema && (id in $currentSchema || dynamicId)}
  <FieldWrapper
    {id}
    let:onBlur
    {label}
    required={isRequired($currentSchema?.[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    {readonly}
  >
    <slot slot="description" name="description" />

    <Uploader {id} {structureSlug} on:blur={onBlur} bind:fileKeys {disabled} />
  </FieldWrapper>
{/if}
