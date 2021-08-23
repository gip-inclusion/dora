<script>
  import Tag from "./_tag.svelte";

  export let service;
</script>

<style>
  .tags-wrapper {
    display: flex;
    flex-direction: row;
    margin-top: var(--s48);
    margin-bottom: var(--s32);
  }

  h2 {
    color: var(--col-france-blue) !important;
  }

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
</style>

<div class="tags-wrapper">
  {#each service.categoriesDisplay as cat}
    <Tag --bg-color="var(--col-magenta-brand)">{cat}</Tag><br />
  {/each}
</div>
<div class="description-wrapper">
  <div>
    <h2>Description du service</h2>
    <strong>{service.shortDesc}</strong>
    <div class="markdown-wrapper prose prose">
      {@html service.fullDesc}
    </div>
  </div>
</div>
