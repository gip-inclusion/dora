<script lang="ts">
  import type { HighlightSegment } from "#lib/utils/highlight.ts";

  interface Props {
    text: string;
    segments?: HighlightSegment[];
  }

  let { text, segments }: Props = $props();
</script>

{#if segments}{#each segments as segment}{#if segment.match}<b>{segment.text}</b
      >{:else}{segment.text}{/if}{/each}{:else}{text}{/if}
