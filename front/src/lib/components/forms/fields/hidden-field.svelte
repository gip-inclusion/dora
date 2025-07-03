<script lang="ts">
  import { currentSchema } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";

  interface Props {
    id: string;
    value?: string | number | undefined;
  }

  let { id, value = $bindable(undefined) }: Props = $props();
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper {id} hidden hideLabel>
    <input type="hidden" bind:value {id} />
  </FieldWrapper>
{/if}
