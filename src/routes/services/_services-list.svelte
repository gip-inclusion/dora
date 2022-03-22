<script>
  import ServiceLine from "$lib/components/services/line.svelte";

  export let services = [];
  export let onRefresh;
  export let showStructure = true;
  export let readOnly = false;
</script>

<div class="flex flex-col gap-s12 pb-s40">
  {#each services as service}
    <ServiceLine {service} {onRefresh} {showStructure} {readOnly} />
  {/each}
</div>
