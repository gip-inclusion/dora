<script>
  import Alert from "$lib/components/forms/alert.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
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
  <CenteredGrid bgColor="bg-gray-bg">
    {#each $formErrors.nonFieldErrors as error}
      <Alert label={error} />
    {/each}
  </CenteredGrid>
{/if}
