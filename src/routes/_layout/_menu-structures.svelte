<script>
  import LinkButton from "$lib/components/link-button.svelte";
  import { shortenString } from "$lib/utils";

  export let structures;
</script>

{#each structures as structure}
  <LinkButton
    label={shortenString(structure.name, 24)}
    to={`/structures/${structure.slug}`}
    noBackground
    small
  />
{/each}
