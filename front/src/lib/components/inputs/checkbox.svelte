<script lang="ts">
  import { createBubbler } from "svelte/legacy";

  const bubble = createBubbler();
  import CheckboxMark from "../display/checkbox-mark.svelte";

  interface Props {
    name: string;
    group: string[];
    label: string;
    value: string;
    disabled?: boolean;
    readonly?: boolean;
    horizontal?: boolean;
    errorMessage?: string | null | undefined;
    focused?: boolean;
    children?: import("svelte").Snippet;
  }

  let {
    name,
    group = $bindable(),
    label,
    value,
    disabled = false,
    readonly = false,
    horizontal = false,
    errorMessage = undefined,
    focused = false,
    children,
  }: Props = $props();

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
  class={`p-s2 flex flex-row items-center rounded-sm ${focused ? "solid 2px #0a76f6" : ""}`}
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
    onchange={handleChange}
    onfocus={bubble("focus")}
    onblur={bubble("blur")}
  />
  <CheckboxMark />
  <span class="ml-s16 text-f16 text-gray-text inline-block">{label}</span>
</label>

{#if children}
  <div class="ml-s42">
    {@render children?.()}
  </div>
{/if}
