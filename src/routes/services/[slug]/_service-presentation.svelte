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

  .maj {
    color: var(--col-text-alt2);
    font-size: var(--f12);
  }
</style>

<div class="tags-wrapper">
  <Tag --bg-color="var(--col-magenta-brand)">{service.categoryDisplay}</Tag>
</div>
<div class="description-wrapper">
  <div>
    <h2>Description du service</h2>
    <strong>{service.shortDesc}</strong>
    <div class="markdown-wrapper prose prose">
      {@html service.fullDesc}
    </div>
    <div class="maj">
      Mise à jour le {new Date(service.modificationDate).toLocaleDateString(
        "fr-FR",
        { year: "numeric", month: "long", day: "numeric" }
      )}
    </div>
  </div>
</div>
