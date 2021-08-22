<script>
  import { contextValidationKey } from "$lib/validation";

  import { getContext } from "svelte";

  import Input from "./input.svelte";
  import Alert from "./alert.svelte";

  export let value = undefined;
  export let name = "";
  export let type;
  export let errorMessages = [];

  export let vertical = false;
  export let label = "";
  export let required = false;
  export let maxLength = undefined;
  export let choices = [];

  export let disabled = undefined;
  export let readonly = false;
  export let visible = true;
  export let placeholder = undefined;
  export let description = "";
  export let minValue = undefined;

  export let hideLabel = false;
  export let toggleYesText = undefined;
  export let toggleNoText = undefined;

  const layoutClass = vertical ? "flex-col " : "flex-row";

  const context = getContext(contextValidationKey);

  function handleBlur(evt) {
    if (context) context.onBlur(evt);
  }
</script>

<style lang="postcss">
  :global(.tag) {
    @apply bg-magenta-80 rounded px-1;
  }
</style>

{#if visible}
  <div class=" flex-1" class:hidden={type === "hidden"}>
    <div
      {name}
      class="flex {layoutClass} items-top relative "
      isDOMLabel={type !== "checkboxes" && type !== "radios"}>
      <div
        class="flex flex-col"
        class:w-250p={!vertical}
        class:w-full={vertical}
        class:mb-1={vertical}>
        <div
          class="inline-block w-full flex-shrink-0 text-base font-bold text-gray-dark">
          <label for={name}>{hideLabel ? "" : label}</label>
          {#if required}<span class="text-error">*</span>{/if}
        </div>
        <span class="text-xs text-gray-text-alt2"> {description}</span>
      </div>
      <div class="flex flex-col flex-1 flex-grow min-h-6">
        {#if type !== "custom"}
          <Input
            on:blur={handleBlur}
            {type}
            {name}
            bind:value
            {choices}
            {maxLength}
            {placeholder}
            {minValue}
            {disabled}
            {readonly}
            {toggleYesText}
            {toggleNoText} />
        {:else}
          <slot name="custom-input" />
        {/if}
        {#each errorMessages || [] as msg}
          <Alert iconOnLeft label={msg} />
        {/each}
      </div>
      <slot name="helptext" />
    </div>
  </div>
{/if}
