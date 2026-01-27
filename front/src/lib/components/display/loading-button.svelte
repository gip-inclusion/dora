<script lang="ts">
  import Button, { type Props as ButtonProps } from "./button.svelte";
  import Spinner from "./spinner.svelte";

  interface Props extends ButtonProps {
    loading: boolean;
  }

  let { loading, ...buttonProps }: Props = $props();
</script>

<div class="inline-grid">
  <div class="col-start-1 row-start-1" class:invisible={loading}>
    <Button {...buttonProps} disabled={loading || buttonProps.disabled} />
  </div>
  {#if loading}
    <div class="col-start-1 row-start-1 flex items-center justify-center">
      <Spinner />
    </div>
  {/if}
</div>
