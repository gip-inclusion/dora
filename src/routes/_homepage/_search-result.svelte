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

  .header {
    padding-left: var(--s16);
    border-left: 4px solid var(--col-available);
  }

  .tags-wrapper {
    display: flex;
    flex-direction: row;
    margin-top: var(--s16);
    margin-bottom: var(--s8);
  }

  p {
    margin-top: var(--s16);
    color: var(--col-text-alt2);
  }
</style>

<div class="wrapper">
  <div class="header">
    <h4><a href="/services/{result.slug}">{result.name}</a></h4>
    <div class="flex flex-row gap-2 mt-1">
      <Label label={`${result.structureName}`} iconOnLeft icon={homeIcon} />

      <Label
        label={`${result.postalCode}, ${result.city}`}
        iconOnLeft
        icon={mapPinIcon} />
    </div>
  </div>
  <p>
    {result.shortDesc}
  </p>
  <div class="tags-wrapper">
    <Tag --bg-color="var(--col-magenta-brand)">{result.categoryDisplay}</Tag
    ><br />
  </div>
</div>
