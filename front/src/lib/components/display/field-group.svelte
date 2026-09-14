<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    title: string;
    children: Snippet;
    showSeparator?: boolean;
  }

  const { title, children, showSeparator = true }: Props = $props();
</script>

<div class="gap-s16 flex flex-col">
  <h3 class="text-f17 text-france-blue leading-32">
    {title}
  </h3>
  {@render children()}
  {#if showSeparator}
    <div class="my-s8">
      <hr />
    </div>
  {/if}
</div>
