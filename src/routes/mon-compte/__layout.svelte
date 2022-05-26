<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Header from "./_header.svelte";
  import { userInfo } from "$lib/auth";
</script>

<svelte:head>
  <meta name="robots" content="noindex" />
</svelte:head>

<CenteredGrid --col-bg="var(--col-gray-dark)">
  <Header name={$userInfo?.fullName} />
</CenteredGrid>

<CenteredGrid
  roundedTop
  --col-under-bg="var(--col-gray-dark)"
  --col-content-bg="var(--col-bg)"
>
  <slot />
</CenteredGrid>
