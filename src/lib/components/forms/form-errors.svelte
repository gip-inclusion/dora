<script lang="ts">
  import Alert from "$lib/components/display/alert.svelte";
  import { formErrors } from "$lib/validation/validation";
  import CenteredGrid from "../display/centered-grid.svelte";
</script>

{#if $formErrors.nonFieldErrors && $formErrors.nonFieldErrors.length}
  <CenteredGrid>
    <div id="nonFieldErrors">
      {#each $formErrors.nonFieldErrors || [] as msg, i}
        <Alert id={`global-errors-${i}`} label={msg} />
      {/each}
    </div>
  </CenteredGrid>
{/if}
