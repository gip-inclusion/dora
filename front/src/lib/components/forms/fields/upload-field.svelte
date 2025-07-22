<!-- @migration-task Error while migrating Svelte code: This migration would change the name of a slot (description to description_1) making the component unusable -->
<script lang="ts">
  import type { Snippet } from "svelte";

  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";

  import FieldWrapper from "../field-wrapper.svelte";
  import Uploader from "../../inputs/uploader.svelte";

  interface Props {
    id: string;
    disabled?: boolean;
    readonly?: boolean;
    label?: string;
    fileKeys?: string[];
    structureSlug?: string;
    descriptionText?: string;
    hidden?: boolean;
    hideLabel?: boolean;
    vertical?: boolean;
    dynamicId?: boolean;
    description?: Snippet;
  }

  let {
    id,
    disabled = false,
    readonly = $currentSchema?.[id]?.readonly,
    label = $currentSchema?.[id]?.label,
    fileKeys = $bindable([]),
    structureSlug = undefined,
    descriptionText = "",
    hidden = false,
    hideLabel = false,
    vertical = false,
    dynamicId = false,
    description,
  }: Props = $props();
</script>

{#if $currentSchema && (id in $currentSchema || dynamicId)}
  <FieldWrapper
    {id}
    {label}
    required={isRequired($currentSchema?.[id], $currentFormData)}
    {descriptionText}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    {readonly}
    {description}
  >
    {#snippet children({ onBlur })}
      <Uploader {id} {structureSlug} onblur={onBlur} bind:fileKeys {disabled} />
    {/snippet}
  </FieldWrapper>
{/if}
