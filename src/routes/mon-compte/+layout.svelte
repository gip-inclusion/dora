<script lang="ts">
  import { userInfo } from "$lib/auth";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Header from "./header.svelte";
</script>

<svelte:head>
  <meta name="robots" content="noindex" />
</svelte:head>

<CenteredGrid bgColor="bg-gray-03">
  <Header name={$userInfo?.fullName} />
</CenteredGrid>

<CenteredGrid>
  <slot />
</CenteredGrid>
