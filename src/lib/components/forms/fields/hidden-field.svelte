<script lang="ts">
  import { currentSchema } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";

  export let id: string;
  export let value: string | number | undefined = undefined;
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper {id} hidden hideLabel>
    <input type="hidden" bind:value {id} />
  </FieldWrapper>
{/if}
