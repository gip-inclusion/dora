<script lang="ts">
  import { formatOsmHours } from "$lib/utils/opening-hours";

  interface Props {
    osmHours: string;
  }

  let { osmHours }: Props = $props();

  const formattedHours = formatOsmHours(osmHours);
</script>

{#if formattedHours}
  <ul>
    {#each formattedHours as [prefix, hourStr]}
      <li class="mb-s8 text-gray-text flex items-center">
        <span class="mr-s16 w-s36">{prefix}</span>
        <span>{hourStr}</span>
      </li>
    {/each}
  </ul>
{:else}
  {osmHours}
{/if}
