<script>
  import Input from "./input.svelte";
  import Label from "./label.svelte";

  export let value = undefined;
  export let selectedItems = undefined;

  export let type;

  export let label = "";
  export let required = false;
  export let choices = [];

  export let placeholder = "";
  export let description = "";
  export let minValue = null;

  export let hideLabel = false;

  $: hiddenClasses = type === "hidden" ? "hidden" : "";
</script>

<style lang="postcss">
  :global(.tag) {
    @apply bg-magenta-80 rounded px-1;
  }
</style>

<!-- svelte-ignore a11y-label-has-associated-control -->
<Label
  className="flex flex-row items-center"
  isDOMLabel={type !== "checkboxes" && type !== "radios"}>
  <span class="{hiddenClasses} inline-block w-17 text-base text-gray-text-alt2">
    {hideLabel ? "" : label}
    {#if required}<span class="text-error">*</span>{/if}
  </span>
  <div class="flex flex-col flex-grow">
    <Input
      {type}
      bind:value
      bind:selectedItems
      {choices}
      {placeholder}
      {description}
      {minValue} />
  </div>
</Label>
