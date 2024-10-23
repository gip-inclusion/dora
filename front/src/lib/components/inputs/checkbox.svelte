<script lang="ts">
  import CheckboxMark from "../display/checkbox-mark.svelte";

  export let name: string;
  export let group: string[];
  export let label: string;
  export let value: string;
  export let disabled = false;
  export let readonly = false;
  export let horizontal = false;
  export let errorMessage: string | null | undefined = undefined;
  export let focused: boolean = false;

  // Malheureusement, utiliser bind:groups ici ne fonctionne pas :
  // https://github.com/sveltejs/svelte/issues/2308
  // La mise à jour de group doit être faite manuellement
  function handleChange(event) {
    const isChecked = event.target.checked;
    if (isChecked && !group.includes(value)) {
      group = [...group, value];
    } else if (!isChecked) {
      group = group.filter((val) => val !== value);
    }
  }
</script>

<label
  class={`flex flex-row items-center rounded p-s2 ${focused ? "solid 2px #0a76f6" : ""}`}
  class:mr-s24={horizontal}
>
  <input
    type="checkbox"
    class="sr-only"
    aria-describedby={errorMessage}
    {name}
    {value}
    {disabled}
    {readonly}
    checked={group.includes(value)}
    on:change={handleChange}
    on:focus
    on:blur
  />
  <CheckboxMark />
  <span class="ml-s16 inline-block text-f16 text-gray-text">{label}</span>
</label>

{#if $$slots.default}
  <div class="ml-s42">
    <slot />
  </div>
{/if}
