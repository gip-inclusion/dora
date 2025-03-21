<script lang="ts">
  import type { ComponentType } from "svelte";

  export let icon: ComponentType;
  export let label: string;
  export let textClass: "text-info" | "text-available" | "text-warning";
</script>

<div class="gap-s8 flex items-center {textClass}">
  <svelte:component this={icon} size={16} />
  {label}
</div>
