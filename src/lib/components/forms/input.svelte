<script>
  import Select from "./select.svelte";

  import RichText from "$lib/components/rich-text/editor.svelte";
  import Toggle from "$lib/components/toggle.svelte";
  import Checkboxes from "./checkboxes.svelte";
  import RadioButtons from "./radio-buttons.svelte";

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
  export let minValue = null;
  export let maxLength = undefined;
  export let rows = 4;

  export let toggleYesText;
  export let toggleNoText;

  export let onSelectChange = undefined;
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
    @apply px-s8 min-h-[3rem] border border-gray-03 rounded outline-none placeholder-gray-text-alt focus:shadow-focus text-f14;
  }

  input,
  textarea {
    @apply disabled:bg-gray-00 read-only:text-gray-03;
  }
</style>

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
    {disabled}
    {readonly}
    {toggleYesText}
    {toggleNoText}
  />
{:else if type === "password"}
  <input
    {name}
    id={name}
    bind:value
    on:blur
    type="password"
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
