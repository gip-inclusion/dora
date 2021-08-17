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
</style>

{#if type === "checkboxes"}
  <div class="flex flex-col gap-1">
    <Checkboxes bind:group={value} {choices} {required} {disabled} />
  </div>
{:else if type === "radios"}
  <div class="flex flex-col gap-1">
    <RadioButtons bind:group={value} {choices} {required} {disabled} />
  </div>
{:else if type === "select"}
  <Select
    {choices}
    on:invalid
    bind:value
    bind:selectedItem
    {placeholder}
    {required}
    {disabled} />
{:else if type === "multiselect"}
  <Select
    {choices}
    on:invalid
    bind:value
    bind:selectedItem
    multiple
    {placeholder}
    {required}
    {disabled} />
{:else if type === "text"}
  <input
    on:invalid
    on:blur
    on:input
    bind:value
    type="text"
    {placeholder}
    {required}
    {disabled} />
{:else if type === "textarea"}
  <textarea
    on:invalid
    on:blur
    on:input
    bind:value
    type="text"
    {maxLength}
    {placeholder}
    {required}
    {disabled}
    rows="4" />
{:else if type === "richtext"}
  <RichText
    bind:htmlContent={value}
    {placeholder}
    initialContent={value}
    {required}
    {disabled} />
{:else if type === "toggle"}
  <Toggle
    bind:checked={value}
    {required}
    {disabled}
    {toggleYesText}
    {toggleNoText} />
{:else if type === "password"}
  <input
    on:invalid
    on:blur
    on:input
    bind:value
    type="password"
    {placeholder}
    {required}
    {disabled} />
{:else if type === "date"}
  <input
    on:invalid
    on:blur
    on:input
    bind:value
    type="date"
    {placeholder}
    {required}
    {disabled} />
{:else if type === "number"}
  <input
    on:invalid
    on:blur
    on:input
    bind:value
    type="number"
    {minValue}
    {placeholder}
    {required}
    {disabled} />
{:else if type === "email"}
  <input
    on:invalid
    on:blur
    on:input
    bind:value
    type="email"
    {placeholder}
    {required}
    {disabled} />
{:else if type === "hidden"}
  <input on:invalid on:blur on:input bind:value type="hidden" {disabled} />
{:else if type === "tel"}
  <input
    on:invalid
    on:blur
    on:input
    bind:value
    type="tel"
    {placeholder}
    {required}
    {disabled} />
{:else if type === "url"}
  <input
    on:invalid
    on:blur
    on:input
    bind:value
    type="url"
    {placeholder}
    {required}
    {disabled} />
{:else if type === "files"}
  <Uploader
    on:invalid
    on:blur
    on:input
    bind:fileKeys={value}
    {required}
    {disabled} />
{/if}
<span />
