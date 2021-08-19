<script>
  import Select from "./select.svelte";

  import RichText from "$lib/components/rich-text/editor.svelte";
  import Toggle from "$lib/components/toggle.svelte";
  import Uploader from "$lib/components/uploader.svelte";
  import Checkboxes from "./checkboxes.svelte";
  import RadioButtons from "./radio-buttons.svelte";

  export let value = undefined;
  export let selectedItem = undefined;

  export let type;
  export let name;

  export let choices = [];

  export let disabled = false;
  export let placeholder = "";
  export let minValue = null;
  export let maxLength = undefined;

  export let toggleYesText;
  export let toggleNoText;
</script>

<style lang="postcss">
  input[type="text"],
  input[type="password"],
  input[type="number"],
  input[type="url"],
  input[type="email"],
  input[type="tel"],
  input[type="date"],
  textarea {
    @apply px-1 min-h-6 border border-gray-03 rounded outline-none placeholder-gray-text-alt focus:shadow-focus text-sm;
  }

  :global(input:disabled, textarea:disabled, select:disabled) {
    background-color: var(--col-gray-00);
  }
</style>

{#if type === "checkboxes"}
  <div class="flex flex-col gap-1">
    <Checkboxes {name} bind:group={value} {choices} {disabled} />
  </div>
{:else if type === "radios"}
  <div class="flex flex-col gap-1">
    <RadioButtons {name} bind:group={value} {choices} {disabled} />
  </div>
{:else if type === "select"}
  <Select
    {name}
    {choices}
    bind:value
    bind:selectedItem
    {placeholder}
    {disabled} />
{:else if type === "multiselect"}
  <Select
    {name}
    {choices}
    bind:value
    bind:selectedItem
    multiple
    {placeholder}
    {disabled} />
{:else if type === "text"}
  <input {name} on:blur bind:value type="text" {placeholder} {disabled} />
{:else if type === "textarea"}
  <textarea
    {name}
    on:blur
    bind:value
    type="text"
    {maxLength}
    {placeholder}
    {disabled}
    rows="4" />
{:else if type === "richtext"}
  <RichText
    {name}
    bind:htmlContent={value}
    {placeholder}
    initialContent={value}
    {disabled} />
{:else if type === "toggle"}
  <Toggle
    {name}
    bind:checked={value}
    {disabled}
    {toggleYesText}
    {toggleNoText} />
{:else if type === "password"}
  <input {name} on:blur bind:value type="password" {placeholder} {disabled} />
{:else if type === "date"}
  <input {name} on:blur bind:value type="date" {placeholder} {disabled} />
{:else if type === "number"}
  <input
    {name}
    on:blur
    bind:value
    type="number"
    min={minValue}
    {placeholder}
    {disabled} />
{:else if type === "email"}
  <input {name} on:blur bind:value type="email" {placeholder} {disabled} />
{:else if type === "hidden"}
  <input {name} on:blur bind:value type="hidden" {disabled} />
{:else if type === "tel"}
  <input {name} on:blur bind:value type="tel" {placeholder} {disabled} />
{:else if type === "url"}
  <input {name} on:blur bind:value type="url" {placeholder} {disabled} />
{:else if type === "files"}
  <Uploader {name} on:blur bind:fileKeys={value} {disabled} />
{/if}
<span />
