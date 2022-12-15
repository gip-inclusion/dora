<script lang="ts">
  import ModelMenu from "$lib/components/specialized/services/model-menu.svelte";
  import { token } from "$lib/utils/auth";

  export let model;
  export let onRefresh;
  const readOnly = !($token && model.canWrite);
</script>

<div class="inline-flex flex-wrap items-start gap-s8">
  <ModelMenu {model} secondary {onRefresh} inline {readOnly} />
</div>
