<script>
  import Input from "./input.svelte";

  export let type;
  export let field;
  export let value;
  export let selectedItems;
  export let placeholder;
  export let noLabel = undefined;
  export let description;
  export let minValue;

  $: required = field.required ? "font-bold" : "";
  $: hidden = type === "hidden" ? "hidden" : "";
</script>

<style lang="postcss">
  :global(.tag) {
    @apply bg-magenta-80 rounded px-1;
  }
</style>

<!-- svelte-ignore a11y-label-has-associated-control -->
<label class="flex flex-row items-center">
  <span
    class="{required} {hidden} inline-block w-17 text-base text-gray-text-alt2">
    {noLabel ? "" : field.label}
  </span>
  <div class="flex flex-col flex-grow">
    <Input
      {type}
      {field}
      {value}
      {selectedItems}
      {placeholder}
      {description}
      {minValue} />
  </div>
</label>
