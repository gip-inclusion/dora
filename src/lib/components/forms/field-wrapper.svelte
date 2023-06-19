<script lang="ts">
  import {
    contextValidationKey,
    formErrors,
    type ValidationContext,
  } from "$lib/validation/validation";
  import { getContext } from "svelte";
  import Alert from "../display/alert.svelte";
  import { randomId } from "$lib/utils/random";

  export let id: string;
  export let label = "";
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let required = false;
  export let vertical = false;
  export let readonly = false;
  export let disabled = false;

  const context = getContext<ValidationContext>(contextValidationKey);

  function handleBlur(evt) {
    if (context) {
      context.onBlur(evt);
    }
  }

  function handleChange(evt) {
    if (context) {
      context.onChange(evt);
    }
  }

  $: errorMessages = $formErrors[id];
  const descriptionId = description ? randomId() : null;
</script>

<div
  class="field-wrapper items-top flex flex-col items-stretch gap-s8 lg:items-start"
  class:lg:flex-row={!vertical}
  class:lg:items-stretch={vertical}
  class:hidden
>
  <div class="label-container flex flex-col" class:one-fourth={!vertical}>
    <label
      for={id}
      class="mt-s8"
      class:sr-only={hideLabel}
      aria-describedby={descriptionId}
    >
      <span class=" text-f17 font-bold text-gray-dark">
        {label}{#if required && !readonly && !disabled}<span
            class="ml-s6 text-error">&nbsp;*</span
          >{/if}
      </span>
    </label>
    {#if description}
      <small id={descriptionId}>{description}</small>
    {/if}
    {#if $$slots.description}
      <div class="mb-s4">
        <slot name="description" />
      </div>
    {/if}
  </div>
  <div class="flex flex-col " class:three-fourths={!vertical}>
    <!-- Slot principal -->
    <slot onBlur={handleBlur} onChange={handleChange} />
    <!--  -->
    {#each errorMessages || [] as msg, i}
      <Alert id="{id}-error-{i}" label={msg} />
    {/each}
  </div>
</div>

<style lang="postcss">
  .one-fourth {
    @apply lg:w-1/3;
  }

  .three-fourths {
    @apply lg:w-2/3;
  }
</style>
