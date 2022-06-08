<script>
  export let service;
</script>

<h2>Description</h2>

<div class="markdown-wrapper prose mb-s24 w-full">
  {@html service.fullDesc}
</div>

<style lang="postcss">
  .markdown-wrapper {
    margin-top: var(--s16);
  }

  .markdown-wrapper :global(h1),
  .markdown-wrapper :global(h2),
  .markdown-wrapper :global(h3) {
    color: var(--col-france-blue);
  }

  .markdown-wrapper :global(p) {
    color: var(--col-text);
  }

  .prose {
    max-width: 100%;
  }
</style>
