<script lang="ts">
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
</script>

<svelte:head>
  <meta name="robots" content="noindex" />
</svelte:head>

<CenteredGrid>
  <h1><a href="/admin">Interface d'administration</a></h1>
  <slot />
</CenteredGrid>
