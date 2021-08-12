<script>
  import AutoComplete from "simple-svelte-autocomplete";
  import { checkIcon } from "$lib/icons.js";

  export let choices;
  export let value = undefined;
  export let selectedItem = undefined;
  export let disabled = false;
  export let placeholder = "";
  export let multiple = false;
  export let hideArrow;
  export let searchFunction;
  export let delay;
  export let localFiltering;
  export let labelFieldName = "displayName";
  export let valueFieldName = "value";
  export let minCharactersToSearch;

  export let onChange;
</script>

<style lang="postcss">
  :global(.autocomplete) {
    @apply h-6 !important;
  }
  :global(.input-container) {
    @apply shadow-none h-6 !important;
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
  {localFiltering}
  {labelFieldName}
  {valueFieldName}
  {minCharactersToSearch}
  {onChange}
  items={choices}
  bind:value
  bind:selectedItem
  {disabled}
  {placeholder}
  {multiple}
  {searchFunction}
  {delay}
  className="rounded focus-within:shadow-focus"
  inputClassName="outline-none border rounded border-gray-03"
  dropdownClassName="mt-2p rounded shadow-md"
  html5autocomplete={false}
  showLoadingIndicator
  {hideArrow}>
  <div slot="item" let:item let:label class="flex flex-row">
    <div class="flex-grow">{@html label}</div>
    <div class="flex-grow-0 hidden checkmark">
      <div class="w-3 h-3 ml-1 fill-current ">{@html checkIcon}</div>
    </div>
  </div>
  <div slot="loading">
    <span class="text-gray-text-alt">Chargement des resultats…</span>
  </div>
  <div slot="no-results">
    <span class="text-error">Aucun resultat</span>
  </div>
</AutoComplete>
