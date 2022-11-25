<script lang="ts">
  import Alert from "$lib/components/forms/alert.svelte";
  import { formErrors } from "$lib/validation";
  import { onDestroy, onMount } from "svelte";

  onMount(() => {
    $formErrors = {};
  });

  onDestroy(() => {
    $formErrors = {};
  });
</script>

{#if $formErrors?.nonFieldErrors?.length}
  {#each $formErrors.nonFieldErrors as error}
    <Alert label={error} />
  {/each}
{/if}
