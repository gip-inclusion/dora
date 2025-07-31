<script lang="ts">
  import type { Component } from "svelte";

  interface Props {
    icon: Component;
    label: string;
    textClass: "text-info" | "text-available" | "text-warning";
  }

  let { icon, label, textClass }: Props = $props();

  const SvelteComponent = $derived(icon);
</script>

<div class="gap-s8 flex items-center {textClass}">
  <SvelteComponent size={16} />
  {label}
</div>
