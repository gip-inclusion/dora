<script lang="ts">
  import TextClamp from "$lib/components/display/text-clamp.svelte";
  import { markdownToHTML } from "$lib/utils/misc";

  export let service;
</script>

<div class="markdown-wrapper prose mb-s24 w-full">
  <TextClamp text={markdownToHTML(service.fullDesc, 4)} />
</div>

<style lang="postcss">
  .markdown-wrapper {
    margin-top: var(--s16);
  }

  .markdown-wrapper :global(h1),
  .markdown-wrapper :global(h2),
  .markdown-wrapper :global(h3) {
    color: var(--col-gray-dark);
  }

  .markdown-wrapper :global(p),
  .markdown-wrapper :global(strong),
  .markdown-wrapper :global(li) {
    color: var(--col-text);
  }

  .prose {
    max-width: 100%;
  }
</style>
