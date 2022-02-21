<script>
  import Select from "./select.svelte";

  import RichText from "$lib/components/rich-text/editor.svelte";
  import Toggle from "$lib/components/toggle.svelte";
  import Checkboxes from "./checkboxes.svelte";
  import RadioButtons from "./radio-buttons.svelte";
  import PasswordInput from "./password-input.svelte";

  export let value = undefined;

  export let type;
  export let name;
  export let autocomplete;
  export let passwordrules;
  export let choices = [];
  export let sortSelect = undefined;

  export let readonly = false;
  export let disabled = false;
  export let placeholder = "";
  export let placeholderMulti = "";
  export let initialValue = undefined;
  export let minValue = null;
  export let maxLength = undefined;
  export let rows = 4;

  export let toggleYesText;
  export let toggleNoText;

  export let onSelectChange = undefined;
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
    onChange={onSelectChange}
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
    onChange={onSelectChange}
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
    {maxLength}
    {placeholder}
    {disabled}
    {readonly}
    {autocomplete}
    {rows}
  />
{:else if type === "richtext"}
  <RichText
    {name}
    bind:htmlContent={value}
    {placeholder}
    initialContent={value}
    {disabled}
    {readonly}
  />
{:else if type === "toggle"}
  <Toggle
    {name}
    bind:checked={value}
    on:change
    {disabled}
    {readonly}
    {toggleYesText}
    {toggleNoText}
  />
{:else if type === "password"}
  <PasswordInput
    on:blur
    {name}
    bind:value
    {placeholder}
    {disabled}
    {readonly}
    {autocomplete}
    {passwordrules}
  />
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
  input[type="password"],
  input[type="number"],
  input[type="url"],
  input[type="email"],
  input[type="tel"],
  input[type="date"],
  textarea {
    @apply rounded border border-gray-03 px-s12 py-s6 text-f14 placeholder-gray-text-alt outline-none focus:shadow-focus;
  }

  input,
  textarea {
    @apply read-only:text-gray-03 disabled:bg-gray-00;
  }
</style>
