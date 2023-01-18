<script lang="ts">
  import type { Shape } from "$lib/validation/schemas/utils";
  import FieldWrapper from "./field-wrapper.svelte";
  import Uploader from "./others/uploader.svelte";

  export let id: string;
  export let schema: Shape<string>;
  export let disabled = false;
  export let readonly = schema?.readonly;

  // Spécifique du select
  export let fileKeys: string[];
  export let structureSlug;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;
</script>

{#if schema}
  <FieldWrapper
    {id}
    let:onBlur
    label={schema.label}
    {description}
    {hidden}
    {hideLabel}
    required={schema.required}
    {vertical}
    {disabled}
    {readonly}
  >
    <Uploader {id} {structureSlug} on:blur={onBlur} bind:fileKeys {disabled} />
  </FieldWrapper>
{/if}
