<script>
  import { getContext } from "svelte";

  import { contextValidationKey } from "$lib/validation";

  import Input from "./input.svelte";
  import Alert from "./alert.svelte";

  export let value = undefined;
  export let name = "";
  export let type;
  export let errorMessages = [];
  export let allowHTMLError = false;
  export let autocomplete = undefined;
  export let passwordrules = undefined;
  export let vertical = false;
  export let label = "";
  export let required = false;
  export let maxLength = undefined;
  export let rows = undefined;
  export let choices = [];
  export let sortSelect = undefined;

  export let disabled = undefined;
  export let readonly = false;
  export let visible = true;
  export let placeholder = undefined;
  export let placeholderMulti = undefined;
  export let description = "";
  export let minValue = undefined;

  export let hideLabel = false;
  export let toggleYesText = undefined;
  export let toggleNoText = undefined;

  export let onSelectChange = undefined;

  const layoutClass = vertical ? "flex-col " : "flex-row";

  const context = getContext(contextValidationKey);

  function handleBlur(evt) {
    if (context) context.onBlur(evt);
  }

  function handleChange(evt) {
    if (context) context.onChange(evt);
  }
</script>

{#if visible}
  <div class="flex-1 " class:hidden={type === "hidden"}>
    <div
      {name}
      class="flex {layoutClass} items-top relative"
      isDOMLabel={type !== "checkboxes" && type !== "radios"}
    >
      <!-- #1# -->
      <div
        class="flex flex-col"
        class:w-s250={!vertical}
        class:w-full={vertical}
        class:mb-s8={vertical}
      >
        <div
          class="shrink-0 inline-block w-full font-bold text-f16 text-gray-dark"
        >
          <label for={name}>{hideLabel ? "" : label}</label>
          {#if required}<span class="text-error">*</span>{/if}
        </div>
        <span class="text-f12 text-gray-text-alt2"> {description}</span>
      </div>
      <div class="flex flex-col flex-1 grow min-h-[3rem]">
        {#if type !== "custom"}
          <Input
            bind:value
            on:blur={handleBlur}
            on:change={handleChange}
            on:change
            on:input
            {onSelectChange}
            {type}
            {name}
            {choices}
            {sortSelect}
            {maxLength}
            {rows}
            {placeholder}
            {placeholderMulti}
            {minValue}
            {disabled}
            {readonly}
            {toggleYesText}
            {toggleNoText}
            {autocomplete}
            {passwordrules}
          />
        {:else}
          <slot name="custom-input" />
        {/if}
        {#each errorMessages || [] as msg}
          <Alert iconOnLeft label={msg} isHTML={allowHTMLError} />
        {/each}
      </div>
      <slot name="helptext" />
    </div>
  </div>
{/if}
