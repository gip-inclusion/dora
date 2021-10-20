<script>
  import Label from "$lib/components/label.svelte";
  import { mapPinIcon, pinDistanceIcon } from "$lib/icons";

  import Tag from "../services/[slug]/_tag.svelte";
  import SearchResultWrapper from "./_search_result_wrapper.svelte";

  export let result;
</script>

<style>
  .header {
    padding-left: var(--s16);
    border-left: 4px solid var(--col-available);
  }

  p {
    margin-top: var(--s16);
    color: var(--col-text-alt2);
  }
</style>

<SearchResultWrapper>
  <div class="header">
    <!-- <a href="/structures/{result.structure}"> -->
    <Label label={result.structureInfo.name} truncate />
    <h4><a href="/services/{result.slug}">{result.name}</a></h4>
    <div class="flex flex-col gap-2 mt-1 md:flex-row">
      <!-- </a> -->
      <Tag --bg-color="var(--col-magenta-20)">{result.categoryDisplay}</Tag>
      <Label
        label={`${result.postalCode}, ${result.city}`}
        iconOnLeft
        icon={mapPinIcon} />
      {#if result.distance}
        <Label
          label={`${result.distance} km`}
          iconOnLeft
          icon={pinDistanceIcon} />
      {/if}
    </div>
  </div>

  <p class="hidden md:block">
    <a href="/services/{result.slug}">{result.shortDesc}</a>
  </p>
</SearchResultWrapper>
