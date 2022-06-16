<script>
  import { token } from "$lib/auth";

  import ModelMenu from "$lib/components/services/model-menu.svelte";

  export let model;
  export let onRefresh;
  const readOnly = !($token && model.canWrite);
</script>

<div class="inline-flex flex-wrap items-start gap-s8">
  <ModelMenu {model} secondary {onRefresh} inline {readOnly} />
</div>
