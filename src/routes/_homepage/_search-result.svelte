<script>
  import Label from "$lib/components/label.svelte";
  import { mapPinIcon, pinDistanceIcon } from "$lib/icons";
  import SearchResultWrapper from "./_search_result_wrapper.svelte";

  export let result;
</script>

<SearchResultWrapper>
  <div class="border-l-4 border-success pl-s16">
    <a href="/structures/{result.structure}">
      <Label label={result.structureInfo.name} truncate />
    </a>
    <h4><a href="/services/{result.slug}">{result.name}</a></h4>
    <div class="mt-s8 flex flex-col gap-s16 md:flex-row">
      <Label label={result.location} icon={mapPinIcon} />
      {#if result.distance}
        <Label label={`${result.distance} km`} icon={pinDistanceIcon} />
      {/if}
    </div>
  </div>

  <p class="mt-s16 hidden text-gray-text-alt2 md:block">
    <a href="/services/{result.slug}">{result.shortDesc}</a>
  </p>
</SearchResultWrapper>
