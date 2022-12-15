<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { userInfo } from "$lib/utils/auth";
  import Header from "./header.svelte";
</script>

<CenteredGrid bgColor="bg-gray-03">
  <Header name={$userInfo?.fullName} />
</CenteredGrid>

<CenteredGrid>
  <slot />
</CenteredGrid>
