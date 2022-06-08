<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Header from "./_header.svelte";
  import { userInfo } from "$lib/auth";
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
