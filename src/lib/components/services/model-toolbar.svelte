<script>
  import { token } from "$lib/auth";

  import ModelMenu from "$lib/components/services/model-menu.svelte";

  export let model;
  export let onRefresh;
</script>

<div class="inline-flex flex-wrap items-start gap-s8">
  {#if $token && model.canWrite}
    <ModelMenu {model} secondary {onRefresh} inline />
  {/if}
</div>
