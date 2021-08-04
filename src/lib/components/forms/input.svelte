<script>
  import Select from "./select.svelte";

  import RichText from "$lib/components/rich-text/editor.svelte";
  import Toggle from "$lib/components/toggle.svelte";
  import Checkboxes from "./checkboxes.svelte";
  import RadioButtons from "./radio-buttons.svelte";

  export let value = undefined;
  export let selectedItems = undefined;

  export let type;

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
    <Checkboxes bind:group={value} {choices} />
  </div>
{:else if type === "radios"}
  <RadioButtons bind:group={value} {choices} />
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
  <Select
    {choices}
    bind:value
    bind:selectedItem={selectedItems}
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
