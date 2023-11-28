<script lang="ts">
  import type { Partner } from "$lib/types";

  export let imgHeight: "small" | "medium" | undefined = undefined;
  export let partnersToShow: Partner[] = [];
</script>

{#each partnersToShow as partner}
  <li class="text-center">
    <img
      class="m-s0 inline"
      class:max-w-[200px]={imgHeight === "medium"}
      class:max-w-[150px]={imgHeight === "small"}
      _src={partner.img}
      alt={partner.name}
    />
  </li>
{/each}
