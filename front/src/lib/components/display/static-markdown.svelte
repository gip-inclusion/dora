<script lang="ts">
  import MarkdownRenderer from "./markdown-renderer.svelte";

  interface Props {
    content: string;
  }

  let { content }: Props = $props();
</script>

<div class="prose max-w-3xl">
  <MarkdownRenderer {content} titleLevel={1} />
</div>

<style lang="postcss">
  @reference "../../../app.css";

  :global(.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6) {
    @apply text-france-blue;
  }
</style>
