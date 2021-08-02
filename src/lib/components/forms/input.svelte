<script>
  import AutoComplete from "simple-svelte-autocomplete";

  import RichText from "$lib/components/rich-text/editor.svelte";
  import Toggle from "$lib/components/toggle.svelte";
  import Checkbox from "./checkbox.svelte";

  export let value = undefined;
  export let selectedItems = undefined;

  export let type;

  export let label = "";
  export let required = false;
  export let choices = [];

  export let placeholder = "";
  export let description = "";
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
    {#each choices as choice}
      <Checkbox group={value} value={choice.value} label={choice.displayName} />
    {/each}
  </div>
{:else if type === "checkbox"}
  <span>{description}</span>
  <Checkbox bind:value {label} />
{:else if type === "radios"}
  {#each choices as choice}
    <label class="flex flex-row items-center">
      <input
        bind:group={value}
        value={choice.value}
        class="inline-block border-gray-02 "
        type="radio" />
      <span class="inline-block w-40 ml-2 ">{choice.displayName}</span>
    </label>
  {/each}
{:else if type === "select"}
  <label class="flex flex-row items-center">
    <select bind:value>
      <option value={null} disabled={required ? "disabled" : ""} selected
        >{placeholder}</option>
      {#each choices as choice}
        <option value={choice.value}>
          {choice.displayName}
        </option>
      {/each}
    </select>
  </label>
{:else if type === "multiselect"}
  <AutoComplete
    items={choices}
    bind:value
    bind:selectedItem={selectedItems}
    labelFieldName="displayName"
    valueFieldName="value"
    disabled={required ? "disabled" : ""}
    inputId={label}
    {placeholder}
    multiple />
{:else if type === "text"}
  <span>{description}</span>
  <input bind:value type="text" {required} />
{:else if type === "richtext"}
  <RichText bind:htmlContent={value} initialContent={value} />
{:else if type === "__multitext__"}
  <span>{description}</span>
  <input bind:value type="text" {required} />
{:else if type === "toggle"}
  <Toggle bind:checked={value} />
{:else if type === "date"}
  <span>{description}</span>
  <input bind:value type="date" />
{:else if type === "number"}
  <span>{description}</span>
  <input bind:value type="number" {minValue} />
{:else if type === "email"}
  <span>{description}</span>
  <input bind:value type="email" />
{:else if type === "hidden"}
  <input bind:value type="hidden" />
{:else if type === "tel"}
  <input bind:value type="tel" />
{:else if type === "url"}
  <input bind:value type="url" />
{/if}
