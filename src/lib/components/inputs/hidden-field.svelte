<script lang="ts">
  import type { Shape } from "$lib/validation/schemas/utils";
  import FieldWrapper from "./field-wrapper.svelte";

  export let id: string;
  export let schema: Shape<string>;

  export let value: any | undefined = undefined;
</script>

{#if schema}
  <FieldWrapper
    let:onBlur
    {id}
    label=""
    hidden
    description=""
    hideLabel
    required={false}
    vertical={false}
  >
    <input type="hidden" bind:value {id} />
  </FieldWrapper>
{/if}
