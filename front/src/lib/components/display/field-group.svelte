<script lang="ts">
  import type { Snippet } from "svelte";
  import InformationLineSystem from "svelte-remix/InformationLineSystem.svelte";
  import Tooltip from "$lib/components/ui/tooltip.svelte";

  interface Props {
    title: string;
    children: Snippet;
    showSeparator?: boolean;
    tooltipContent?: Snippet;
  }

  const {
    title,
    children,
    showSeparator = true,
    tooltipContent,
  }: Props = $props();
</script>

<div class="flex flex-col">
  <div class="flex-start gap-s4 flex flex-row items-center">
    <h3 class="text-f17 text-france-blue mb-s0">
      {title}
    </h3>
    {#if tooltipContent}
      <Tooltip content={tooltipContent}>
        <InformationLineSystem />
      </Tooltip>
    {/if}
  </div>
  <div class="gap-s16 flex flex-col">
    {@render children()}
    {#if showSeparator}
      <div class="my-s8">
        <hr />
      </div>
    {/if}
  </div>
</div>
