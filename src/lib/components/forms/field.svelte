<script>
  import Input from "./input.svelte";
  import Label from "./label.svelte";

  export let value = undefined;
  export let selectedItem = undefined;

  export let type;

  export let vertical = false;
  export let label = "";
  export let required = false;
  export let choices = [];

  export let disabled = undefined;
  export let placeholder = "";
  export let description = "";
  export let minValue = null;

  export let hideLabel = false;
  export let toggleYesText;
  export let toggleNoText;

  let layoutClass = vertical ? "flex-col " : "flex-row";
  $: hiddenClasses = type === "hidden" ? "hidden" : "";
</script>

<style lang="postcss">
  :global(.tag) {
    @apply bg-magenta-80 rounded px-1;
  }
</style>

<div class:hidden={type == "hidden"} class="flex-grow">
  <Label
    className="flex {layoutClass} items-top relative "
    isDOMLabel={type !== "checkboxes" && type !== "radios"}>
    <div
      class="flex flex-col"
      class:w-250p={!vertical}
      class:w-full={vertical}
      class:mb-2={vertical}>
      <div
        class="{hiddenClasses} inline-block w-17 flex-shrink-0 text-base font-bold text-gray-dark"
        class:w-17={!vertical}>
        {hideLabel ? "" : label}
        {#if required}<span class="text-error">*</span>{/if}
      </div>
      <span class="text-xs text-gray-text-alt2"> {description}</span>
    </div>
    <div class="flex flex-col flex-grow min-h-6">
      <slot name="input">
        <Input
          {type}
          bind:value
          bind:selectedItem
          {choices}
          {placeholder}
          {minValue}
          {disabled}
          {toggleYesText}
          {toggleNoText} />
      </slot>
    </div>
    <slot name="helptext" />
  </Label>
</div>
