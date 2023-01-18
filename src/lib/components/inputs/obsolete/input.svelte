<script lang="ts">
  import RichText from "$lib/components/inputs/rich-text/editor.svelte";
  import Toggle from "$lib/components/inputs/others/toggle.svelte";
  import type { InputType } from "$lib/types";
  import Checkboxes from "../others/checkboxes.svelte";
  import RadioButtons from "../others/radio-buttons.svelte";
  import Select from "../select/select.svelte";

  export let value = undefined;

  export let type: InputType;
  export let name;
  export let autocomplete;
  export let choices = [];
  export let sortSelect = undefined;

  export let readonly = false;
  export let disabled = false;
  export let placeholder = "";
  export let placeholderMulti = "";
  export let initialValue = undefined;
  export let minValue = null;
  export let rows = 4;

  export let onChange = undefined;
</script>

{#if type === "checkboxes"}
  <Checkboxes
    {name}
    bind:group={value}
    on:change
    {choices}
    {disabled}
    {readonly}
  />
{:else if type === "radios"}
  <RadioButtons
    {name}
    bind:group={value}
    on:change
    {choices}
    {disabled}
    {readonly}
  />
{:else if type === "select"}
  <Select
    {name}
    {choices}
    sort={sortSelect}
    bind:value
    on:blur
    {onChange}
    {placeholder}
    {placeholderMulti}
    {disabled}
    {readonly}
    {initialValue}
  />
{:else if type === "multiselect"}
  <Select
    {name}
    {choices}
    sort={sortSelect}
    bind:value
    on:blur
    {onChange}
    multiple
    {placeholder}
    {placeholderMulti}
    {disabled}
    {readonly}
    {initialValue}
  />
{:else if type === "text"}
  <input
    {name}
    id={name}
    bind:value
    on:blur
    on:input
    type="text"
    {placeholder}
    {disabled}
    {readonly}
    {autocomplete}
  />
{:else if type === "textarea"}
  <textarea
    {name}
    id={name}
    bind:value
    on:blur
    type="text"
    {placeholder}
    {disabled}
    {readonly}
    {autocomplete}
    {rows}
  />
{:else if type === "richtext"}
  <RichText
    id={name}
    {name}
    bind:htmlContent={value}
    {placeholder}
    initialContent={value}
    {disabled}
    {readonly}
  />
{:else if type === "toggle"}
  <Toggle {name} bind:checked={value} on:change {disabled} {readonly} />
{:else if type === "date"}
  <input
    {name}
    id={name}
    bind:value
    on:blur
    type="date"
    {placeholder}
    {disabled}
    {readonly}
    {autocomplete}
  />
{:else if type === "number"}
  <input
    {name}
    id={name}
    bind:value
    on:blur
    type="number"
    min={minValue}
    {placeholder}
    {disabled}
    {readonly}
    {autocomplete}
  />
{:else if type === "email"}
  <input
    {name}
    id={name}
    bind:value
    on:blur
    type="email"
    {placeholder}
    {disabled}
    {readonly}
    {autocomplete}
  />
{:else if type === "hidden"}
  <input
    {name}
    id={name}
    bind:value
    on:blur
    type="hidden"
    {disabled}
    {readonly}
    {autocomplete}
  />
{:else if type === "tel"}
  <input
    {name}
    id={name}
    bind:value
    on:blur
    type="tel"
    {placeholder}
    {disabled}
    {readonly}
    {autocomplete}
  />
{:else if type === "url"}
  <input
    {name}
    id={name}
    bind:value
    on:blur
    type="url"
    {placeholder}
    {disabled}
    {readonly}
    {autocomplete}
  />
{/if}
<span />

<style lang="postcss">
  input[type="text"],
  input[type="number"],
  input[type="url"],
  input[type="email"],
  input[type="tel"],
  input[type="date"],
  textarea {
    @apply min-h-[3rem] rounded border border-gray-03 px-s12 py-s6 text-f14 placeholder-gray-text-alt outline-none focus:shadow-focus;
  }

  input,
  textarea {
    @apply grow read-only:text-gray-03 disabled:bg-gray-00;
  }
</style>
