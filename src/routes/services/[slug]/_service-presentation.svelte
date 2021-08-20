<script>
  import Tag from "./_tag.svelte";

  export let service;
</script>

<div class="flex flex-row">
  {#each service.kindsDisplay as kind}
    <Tag --bg-color="var(--col-magenta-20)">{kind}</Tag>
  {/each}
  {#each service.categoriesDisplay as cat}
    <Tag --bg-color="var(--col-magenta-40)">{cat}</Tag><br />
  {/each}
</div>
<div class="flex flex-row">
  <div>
    <h2>Description du service</h2>
    <strong>{service.shortDesc}</strong>
    {@html service.fullDesc}
  </div>
</div>
