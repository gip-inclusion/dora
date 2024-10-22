<script lang="ts">
  import { markdownToHTML } from "$lib/utils/misc";
  export let content;
</script>

<div class="prose max-w-3xl">
  {@html markdownToHTML(content, 1)}
</div>

<style lang="postcss">
  :global(.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6) {
    @apply text-france-blue;
  }
</style>
