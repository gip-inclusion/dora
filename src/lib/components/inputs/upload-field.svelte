<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "./field-wrapper.svelte";
  import Uploader from "./others/uploader.svelte";

  export let id: string;
  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;

  // Spécifique du select
  export let fileKeys: string[];
  export let structureSlug;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    let:onBlur
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    {readonly}
  >
    <Uploader {id} {structureSlug} on:blur={onBlur} bind:fileKeys {disabled} />
  </FieldWrapper>
{/if}
