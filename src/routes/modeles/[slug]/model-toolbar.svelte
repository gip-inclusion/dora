<script lang="ts">
  import ModelMenu from "$lib/components/specialized/services/model-menu.svelte";

  export let model;
  export let onRefresh;
  const readOnly = !model.canWrite;
</script>

<div class="inline-flex flex-wrap items-start gap-s8">
  <ModelMenu {model} secondary {onRefresh} inline {readOnly} />
</div>
