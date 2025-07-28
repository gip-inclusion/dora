<script lang="ts">
  import type { Partner } from "$lib/types";

  interface Props {
    imgHeight?: "small" | "medium";
    partnersToShow?: Partner[];
  }

  let { imgHeight, partnersToShow = [] }: Props = $props();
</script>

{#each partnersToShow as partner}
  <li class="text-center">
    <img
      class="m-s0 inline"
      class:max-w-[200px]={imgHeight === "medium"}
      class:max-w-[150px]={imgHeight === "small"}
      src={partner.img}
      alt={partner.name}
    />
  </li>
{/each}
