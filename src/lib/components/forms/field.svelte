<script>
  import AutoComplete from "simple-svelte-autocomplete";

  import Tiptap from "$lib/tiptap.svelte";
  import Toggle from "$lib/components/toggle.svelte";
  export let type;
  export let field;
  export let value;
  export let selectedItems = undefined;
  export let placeholder = undefined;
  export let noLabel = undefined;
  export let description = "";
  export let min = undefined;
</script>

<style>
  :global(.tag) {
    @apply bg-red-300 rounded px-1;
  }
</style>

<!-- svelte-ignore a11y-label-has-associated-control -->
<label class="flex flex-row items-center">
  {#if field}
    <span
      class="inline-block w-40 {field.required ? 'font-bold' : ''} {type ===
      'hidden'
        ? 'hidden'
        : ''}">{noLabel ? "" : field.label}</span>
    <div class="flex flex-col flex-grow">
      {#if type === "checkboxes"}
        {#each field.child?.choices || field.choices as choice}
          <label class="flex flex-row items-center">
            <input
              bind:group={value}
              value={choice.value}
              class="inline-block border-gray-300 "
              type="checkbox" />
            <span class="inline-block w-40 ml-2 ">{choice.displayName}</span>
          </label>
        {/each}
      {:else if type === "radios"}
        {#each field.child?.choices || field.choices as choice}
          <label class="flex flex-row items-center">
            <input
              bind:group={value}
              value={choice.value}
              class="inline-block border-gray-300 "
              type="radio" />
            <span class="inline-block w-40 ml-2 ">{choice.displayName}</span>
          </label>
        {/each}
      {:else if type === "select"}
        <label class="flex flex-row items-center">
          <select bind:value>
            <option
              value={null}
              disabled={field.required ? "disabled" : ""}
              selected>{placeholder}</option>
            {#each field.child?.choices || field.choices as choice}
              <option value={choice.value}>
                {choice.displayName}
              </option>
            {/each}
          </select>
        </label>
      {:else if type === "multiselect"}
        <AutoComplete
          items={field.child?.choices || field.choices}
          bind:value
          bind:selectedItem={selectedItems}
          labelFieldName="displayName"
          valueFieldName="value"
          disabled={field.required ? "disabled" : ""}
          inputId={field.label}
          {placeholder}
          multiple />
      {:else if type === "text"}
        <span>{description}</span>
        <input bind:value type="text" required={field.required} />
      {:else if type === "richtext"}
        <Tiptap
          bind:htmlContent={value}
          initialContent={value}
          className="prose prose-sm p-2 bg-white whitespace-pre-wrap w-full max-w-none h-64 border-2 overflow-auto focus:outline-none" />
      {:else if type === "__multitext__"}
        <span>{description}</span>
        <input bind:value type="text" required={field.required} />
      {:else if type === "toggle"}
        <Toggle bind:checked={value} />
      {:else if type === "date"}
        <span>{description}</span>
        <input bind:value type="date" />
      {:else if type === "number"}
        <span>{description}</span>
        <input bind:value type="number" {min} />
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
    </div>
  {/if}
</label>
