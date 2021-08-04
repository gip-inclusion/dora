<script>
  import AutoComplete from "simple-svelte-autocomplete";
  import { checkIcon } from "$lib/icons.js";

  export let choices;
  export let value = undefined;
  export let selectedItem = undefined;
  export let disabled = false;
  export let placeholder = "";
  export let multiple = false;
</script>

<style lang="postcss">
  :global(.input-container) {
    @apply shadow-none !important;
  }
  :global(.autocomplete-list) {
    @apply border-none !important;
  }
  :global(.autocomplete-list-item) {
    @apply text-gray-text-alt !important;
  }

  :global(.autocomplete-list-item.confirmed) {
    @apply text-dora-magenta-cta bg-white !important;
  }

  :global(.autocomplete-list-item.selected) {
    @apply text-gray-text bg-gray-bg !important;
  }

  :global(.autocomplete-list-item.selected.confirmed) {
    @apply text-dora-magenta-cta bg-gray-bg !important;
  }

  :global(.autocomplete-list-item.confirmed .checkmark) {
    @apply block !important;
  }
</style>

<AutoComplete
  items={choices}
  bind:value
  bind:selectedItem
  labelFieldName="displayName"
  valueFieldName="value"
  {disabled}
  {placeholder}
  {multiple}
  className="rounded  focus-within:shadow-focus "
  inputClassName="outline-none border rounded border-gray-03"
  dropdownClassName="mt-2p rounded shadow-md !important"
  html5autocomplete={false}
  showLoadingIndicator>
  <div slot="item" let:item let:label class="flex flex-row">
    <div class="flex-grow">{@html label}</div>
    <div class="flex-grow-0 hidden checkmark">
      <div class="w-3 h-3 ml-1 fill-current ">{@html checkIcon}</div>
    </div>
  </div>
</AutoComplete>
