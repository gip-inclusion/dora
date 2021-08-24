<script>
  import Label from "$lib/components/label.svelte";
  import { mapPinIcon, homeIcon } from "$lib/icons";

  import Tag from "../services/[slug]/_tag.svelte";

  export let result;
</script>

<style>
  .wrapper {
    padding: 20px 20px 24px 24px;
    background-color: var(--col-white);
    border-radius: var(--s8);
    box-shadow: var(--shadow-sm);
  }

  .tags-wrapper {
    display: flex;
    flex-direction: row;
    margin-top: var(--s48);
    margin-bottom: var(--s32);
  }
</style>

<div class="wrapper">
  <h4><a href="/services/{result.slug}">{result.name}</a></h4>
  <div class="flex flex-row">
    <Label label={`${result.structureName}`} iconOnLeft icon={homeIcon} />

    <Label
      label={`${result.postalCode}, ${result.city}`}
      iconOnLeft
      icon={mapPinIcon} />
  </div>
  <p>
    {result.shortDesc}
  </p>
  <div class="tags-wrapper">
    {#each result.categoryDisplay as cat}
      <Tag --bg-color="var(--col-magenta-brand)">{cat}</Tag><br />
    {/each}
  </div>
</div>
