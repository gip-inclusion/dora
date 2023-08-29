<script lang="ts">
  import { formatOsmHours } from "$lib/utils/opening-hours";

  export let osmHours: string;
</script>

<ul>
  {#each formatOsmHours(osmHours) as [prefix, hourStr]}
    <li class="mb-s8 flex items-center text-gray-text">
      <span class="mr-s16 w-s35">{prefix}</span>
      <span>{hourStr}</span>
    </li>
  {/each}
</ul>
