<script>
  import Alert from "$lib/components/forms/alert.svelte";
  import { onMount, onDestroy } from "svelte";

  import { formErrors } from "$lib/validation.js";

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
