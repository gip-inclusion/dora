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

  export let required = false;
  export let choices = [];

  export let disabled = undefined;
  export let placeholder = "";
  export let minValue = null;
</script>

<style lang="postcss">
  input[type="text"],
  input[type="number"],
  input[type="url"],
  input[type="email"],
  input[type="tel"],
  input[type="date"] {
    @apply px-1 py-3/4 border border-gray-03 rounded outline-none placeholder-gray-text-alt focus:shadow-focus;
  }
</style>

{#if type === "checkboxes"}
  <div class="flex flex-col gap-1/2">
    <Checkboxes bind:group={value} {choices} {disabled} />
  </div>
{:else if type === "radios"}
  <div class="flex flex-col gap-1/2">
    <RadioButtons bind:group={value} {choices} {disabled} />
  </div>
{:else if type === "select"}
  <Select {choices} bind:value bind:selectedItem {placeholder} {disabled} />
{:else if type === "multiselect"}
  <Select
    {choices}
    bind:value
    bind:selectedItem
    {placeholder}
    multiple
    {disabled} />
{:else if type === "text"}
  <input bind:value type="text" {placeholder} {required} {disabled} />
{:else if type === "richtext"}
  <RichText
    bind:htmlContent={value}
    {placeholder}
    initialContent={value}
    {disabled} />
{:else if type === "__multitext__"}
  <input bind:value type="text" {required} {disabled} />
{:else if type === "toggle"}
  <Toggle bind:checked={value} {disabled} />
{:else if type === "date"}
  <input bind:value type="date" {disabled} />
{:else if type === "number"}
  <input bind:value type="number" {minValue} {disabled} />
{:else if type === "email"}
  <input bind:value type="email" {disabled} />
{:else if type === "hidden"}
  <input bind:value type="hidden" {disabled} />
{:else if type === "tel"}
  <input bind:value type="tel" {disabled} />
{:else if type === "url"}
  <input bind:value type="url" {disabled} />
{:else if type === "files"}
  <Uploader bind:fileKeys={value} {disabled} />
{/if}
