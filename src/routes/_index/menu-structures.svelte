<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { capitalize, shortenString } from "$lib/utils/misc";

  export let structures;
</script>

{#each structures as structure}
  <LinkButton
    label={shortenString(capitalize(structure.name), 24)}
    to={`/structures/${structure.slug}`}
    noBackground
    small
  />
{/each}
