<script lang="ts">
  import { getAbTestingUserGroup } from "$lib/utils/ab-testing";

  export let abTestingName: string;
  export let showIfGroups: string[] = [];

  const userGroup = getAbTestingUserGroup(abTestingName);
</script>

{#if showIfGroups.includes(userGroup)}
  <slot />
{/if}
