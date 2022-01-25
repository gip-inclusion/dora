<script>
  import Label from "$lib/components/label.svelte";
  import { mapPinIcon, pinDistanceIcon } from "$lib/icons";

  import Tag from "$lib/components/tag.svelte";
  import SearchResultWrapper from "./_search_result_wrapper.svelte";

  export let result;
</script>

<SearchResultWrapper>
  <div class="header">
    <a href="/structures/{result.structure}">
      <Label label={result.structureInfo.name} truncate />
    </a>
    <h4><a href="/services/{result.slug}">{result.name}</a></h4>
    <div class="flex flex-col gap-s16 mt-s8 md:flex-row">
      <Tag selfStart>
        {result.categoryDisplay}
      </Tag>
      <Label
        label={`${result.postalCode}, ${result.city}`}
        iconOnLeft
        icon={mapPinIcon}
      />
      {#if result.distance}
        <Label
          label={`${result.distance} km`}
          iconOnLeft
          icon={pinDistanceIcon}
        />
      {/if}
    </div>
  </div>

  <div class="paragraph-small text-gray-text-alt2 mt-s16 hidden md:block">
    <a href="/services/{result.slug}">{result.shortDesc}</a>
  </div>
</SearchResultWrapper>

<style lang="postcss">
  .header {
    padding-left: var(--s16);
    border-left: 4px solid var(--col-available);
  }
</style>
