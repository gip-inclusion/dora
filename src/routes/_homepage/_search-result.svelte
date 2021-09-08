<script>
  import Label from "$lib/components/label.svelte";
  import { mapPinIcon, homeIcon, pinDistanceIcon } from "$lib/icons";
  import { shortenString } from "$lib/utils";

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
      <a href="/structures/{result.structure}">
        <Label
          label={shortenString(result.structureInfo.name)}
          iconOnLeft
          icon={homeIcon} />
      </a>
      <Label
        label={`${result.postalCode}, ${result.city}`}
        iconOnLeft
        icon={mapPinIcon} />
      <Label
        label={`${result.distance} km`}
        iconOnLeft
        icon={pinDistanceIcon} />
    </div>
  </div>
  <p><a href="/services/{result.slug}">{result.shortDesc}</a></p>
  <div class="tags-wrapper">
    <Tag --bg-color="var(--col-magenta-brand)">{result.categoryDisplay}</Tag
    ><br />
  </div>
</div>
